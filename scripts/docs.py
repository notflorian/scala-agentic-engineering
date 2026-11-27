#!/usr/bin/env python3
"""Split the editorial guide, track translations, and stage the Jekyll source."""

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import sys
import unicodedata
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("en", "fr", "es", "pt", "it", "de")
FENCE = re.compile(r"^((?: {0,3}>[ \t]?)* {0,3})(`{3,}|~{3,})([^\r\n]*)$")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)[ \t]*$")
CHAPTER = re.compile(r"^(\d+[A-Z]?)\.\s")
INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)
URL = re.compile(r"https?://[^\s<>`]+")
NUMBER = re.compile(r"\d+(?:[.,:\-–]\d+)*(?:[ \u00a0\u202f]\d{3}(?!\d))*")
MARKER = re.compile(r"^<!-- section: ([a-z0-9-]+) -->\n", re.M)


@dataclass(frozen=True)
class Section:
    chapter: str
    key: str
    text: str

    @property
    def heading(self):
        return HEADING.fullmatch(self.text.splitlines()[0]) if self.key else None


def pieces(text):
    """Yield lines outside fences and whole fenced blocks with their language."""
    lines = text.splitlines(keepends=True)
    index = 0
    while index < len(lines):
        line = lines[index]
        fence = FENCE.fullmatch(line.rstrip("\r\n"))
        if not fence or (fence[2].startswith("`") and "`" in fence[3]):
            yield None, line
            index += 1
            continue
        start = index
        quote_prefix = r"(?: {0,3}>[ \t]?){" + str(fence[1].count(">")) + r"}"
        closer = re.compile(quote_prefix + r" {0,3}" + fence[2][0] + r"{" + str(len(fence[2])) + r",}[ \t]*$")
        index += 1
        while index < len(lines) and not closer.fullmatch(lines[index].rstrip("\r\n")):
            index += 1
        if index == len(lines):
            raise ValueError(f"Unclosed Markdown fence at line {start + 1}")
        index += 1
        yield fence[3].strip(), "".join(lines[start:index])



def prose_blocks(text):
    """Group adjacent nonblank lines, leaving fence blocks untouched."""
    pending = []
    for fence, chunk in pieces(text):
        if fence is None and chunk.strip():
            pending.append(chunk)
            continue
        if pending:
            yield None, "".join(pending)
            pending.clear()
        yield fence, chunk
    if pending:
        yield None, "".join(pending)

def parse_source(text):
    chapter, key = "home", ""
    number_seen = (0, "")
    parts, lines, seen = [], [], Counter()
    for fence, chunk in pieces(text):
        heading = HEADING.fullmatch(chunk.rstrip("\r\n")) if fence is None else None
        if heading:
            if lines:
                parts.append(Section(chapter, key, "".join(lines)))
                lines = []
            level, title = len(heading[1]), heading[2]
            number = CHAPTER.match(title) if level == 1 else None
            if number:
                value = re.fullmatch(r"(\d+)([A-Z]?)", number[1])
                number_key = int(value[1]), value[2]
                # The chapter sequence is ascending. The worktree recipe in
                # chapter 12 uses its own numbered H1s from 1 through 7.
                if number_key > number_seen:
                    chapter = "ch-" + number[1].lower()
                    number_seen = number_key
            key = f"{level}:{title}"
            seen[chapter, key] += 1
            if seen[chapter, key] > 1:
                key += f" [{seen[chapter, key]}]"
        lines.append(chunk)
    if lines:
        parts.append(Section(chapter, key, "".join(lines)))
    return parts


def allocate_ids(sections, registry):
    """Retain retired entries so existing anchors never move or get reused."""
    result = json.loads(json.dumps(registry))
    seen = set()
    for part in sections:
        record = result.setdefault(part.chapter, {"next": 1, "headings": {}})
        root = "chapter" if part.chapter != "home" else "guide"
        default = "preamble"
        if part.heading:
            default = root if part.chapter not in seen else f"s-{record['next']}"
            seen.add(part.chapter)
        if part.key not in record["headings"]:
            if default in record["headings"].values():
                raise ValueError(f"{part.chapter}: rename the existing heading key in sections.json")
            record["headings"][part.key] = default
            if default.startswith("s-"):
                record["next"] += 1
    return result


def digest(text):
    return sha256(text.encode("utf-8")).hexdigest()


def load_json(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def translation_status(source, translated, record):
    if source is None:
        return "deleted"
    if translated is None:
        return "missing"
    if record is None:
        return "untracked"
    if record["source_sha256"] != source:
        return "stale"
    if record["translation_sha256"] != translated:
        return "modified"
    return "current"


def inline_parts(line):
    position = 0
    for match in INLINE_CODE.finditer(line):
        yield False, line[position:match.start()]
        yield True, match[0]
        position = match.end()
    yield False, line[position:]


def markdown_url(match):
    return match.rstrip(".,;:!?)]}»”")



def numeric_values(span):
    """Capture numerical values together with signs, currencies, and percent units."""
    urls = [match.span() for match in URL.finditer(span)]
    for match in NUMBER.finditer(span):
        if any(start <= match.start() < end for start, end in urls):
            continue
        before, after = match.span()
        prefix = re.search(r"[$€£¥][ \t]*$|(?<![\w.])[+−–~-]$", span[:before])
        suffix = re.match(r"[ \t\u00a0\u202f]*(?:%|[€$£¥](?!\d))", span[after:])
        start = prefix.start() if prefix else before
        end = after + suffix.end() if suffix else after
        yield start, end, match[0], prefix[0] if prefix else "", suffix[0] if suffix else ""

def signature(text):
    """Compare literal code, links, numeric tokens and Markdown block structure."""
    blocks, code, urls, numbers = [], [], Counter(), Counter()
    for fence, chunk in prose_blocks(text):
        if fence is not None:
            blocks.append(("fence", fence))
            code.append(chunk)
            continue
        for line in chunk.splitlines():
            heading = HEADING.fullmatch(line)
            if heading:
                blocks.append(("heading", len(heading[1])))
                continue
            prefix = re.match(r"^( *)(?:(> *)+|([-+*]|\d+[.)]) +)", line)
            if prefix:
                blocks.append(("prefix", prefix[0].strip(), len(prefix[1])))
            if line.lstrip().startswith("|"):
                blocks.append(("table", len(re.findall(r"(?<!\\)\|", line))))
            if re.fullmatch(r" {0,3}(?:-{3,}|\*{3,}|_{3,})\s*", line):
                blocks.append(("rule", line.strip()))
        for literal, span in inline_parts(chunk):
            if literal:
                code.append(span.replace("\n", " "))
                continue
            urls.update(markdown_url(match[0]) for match in URL.finditer(span))
            urls.update(match[1] for match in re.finditer(r"\]\(([^\s)]+)", span)
                        if not match[1].startswith(("http:", "https:")))
            urls.update(match[1] for match in re.finditer(r"^ {0,3}\[[^\]]+\]:\s*([^\s]+)", span, re.M)
                        if not match[1].startswith(("http:", "https:")))
            numbers.update((value, prefix.strip().replace("−", "-").replace("–", "-"), suffix.strip())
                           for _, _, value, prefix, suffix in numeric_values(span))
    return blocks, code, urls, numbers


def rewrite_links(text, language, chapter, aliases, baseurl=""):
    def destination(value):
        path, separator, fragment = value.partition("#")
        if path not in ("", "guide.md", "./guide.md"):
            return value
        if path and not separator:
            return f"{baseurl}/{language}/"
        if not separator:
            return value
        fragment = unquote(fragment)
        if fragment not in aliases:
            return value
        target, anchor = aliases[fragment]
        if target == chapter:
            return f"#{anchor}"
        prefix = f"{baseurl}/{language}/"
        return f"{prefix if target == 'home' else prefix + target + '/'}#{anchor}"

    def rewrite(span):
        span = re.sub(r"(\]\(<?)([^\s)>]+)", lambda m: m[1] + destination(m[2]), span)
        return re.sub(r"^( {0,3}\[[^\]]+\]:\s*<?)([^\s>]+)", lambda m: m[1] + destination(m[2]), span, flags=re.M)

    return "".join(chunk if fence is not None else "".join(
        span if literal else rewrite(span) for literal, span in inline_parts(chunk)
    ) for fence, chunk in prose_blocks(text))



def render_prose(text):
    """Resolve Markdown ambiguities before rendering; literal examples stay intact."""
    def prose(span, offset, original):
        pattern = re.compile(r"(?<!\\)\||" + URL.pattern)

        def format_match(match):
            value = match[0]
            position = offset + match.start()
            if value == "|":
                line_start = original.rfind("\n", 0, position) + 1
                if original[line_start:].lstrip(" \t").startswith("|"):
                    return value
                return "\\|"
            if original[max(0, position - 2):position] in {"](", '=\"', "='"} or (position and original[position - 1] == "<"):
                return value
            target = markdown_url(value)
            return f"<{target}>" + value[len(target):]

        return pattern.sub(format_match, span)

    result = []
    for fence, chunk in prose_blocks(text):
        if fence is not None:
            result.append(chunk)
            continue
        offset = 0
        rendered = []
        for literal, span in inline_parts(chunk):
            rendered.append(span if literal else prose(span, offset, chunk))
            offset += len(span)
        result.append(re.sub(r"(?m)(?<=\S\n)(---)(?=\n|$)", r"\n\1", "".join(rendered)))
    return "".join(result)


def slug(title):
    title = re.sub(r"`([^\x60]+)`", r"\1", title.lower())
    title = re.sub(r"[^\w\s-]", "", title)
    return re.sub(r"\s", "-", title.strip())


def alias_map(source, registry):
    by_chapter, global_aliases = defaultdict(dict), {}
    seen = Counter()
    for section in source:
        if not section.heading:
            continue
        anchor = registry[section.chapter]["headings"][section.key]
        target = section.chapter, anchor
        title = section.heading[2]
        for variant in sorted({slug(title), slug(unicodedata.normalize("NFKD", title))}):
            qualifier = seen[variant]
            if qualifier:
                global_aliases[f"{variant}-{qualifier}"] = target
            else:
                global_aliases.setdefault(variant, target)
            seen[variant] += 1
        by_chapter[section.chapter][anchor] = target
    return {section.chapter: global_aliases | by_chapter[section.chapter] for section in source}


def read_translation(path):
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    markers = list(MARKER.finditer(text))
    if not markers or text[:markers[0].start()].strip():
        raise ValueError(f"{path}: expected section markers")
    result = {}
    for index, marker in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        if marker[1] in result:
            raise ValueError(f"{path}: duplicate section {marker[1]}")
        result[marker[1]] = text[marker.end():end]
    return result


def translation_path(language, chapter):
    return ROOT / "translations" / language / f"{chapter}.md"


def records_path(language, chapter):
    return ROOT / "translations" / language / f"{chapter}.json"


def sources():
    source = parse_source((ROOT / "guide.md").read_bytes().decode("utf-8"))
    path = ROOT / "translations" / "sections.json"
    registry = load_json(path, {})
    return source, path, registry


def group_source(source, registry):
    grouped = defaultdict(dict)
    for part in source:
        anchor = registry[part.chapter]["headings"][part.key]
        if anchor in grouped[part.chapter]:
            raise ValueError(f"{part.chapter}: duplicate anchor {anchor}")
        grouped[part.chapter][anchor] = part.text
    return grouped


def record(language, chapter, source, checked, only=None):
    translated = read_translation(translation_path(language, chapter))
    records = load_json(records_path(language, chapter), {})
    if checked:
        for section_id in set(records) - set(source):
            if section_id not in translated:
                del records[section_id]
    for section_id, content in source.items():
        if only and section_id not in only:
            continue
        target = translated.get(section_id)
        if not target or signature(content) != signature(target):
            raise ValueError(f"{language}/{chapter}#{section_id}: missing text or changed structure, code, links or numbers")
        if content.strip() == target.strip() and re.search(r"[^\W\d_]{3}", content):
            raise ValueError(f"{language}/{chapter}#{section_id}: identical to French")
        records[section_id] = {"source_sha256": digest(content), "translation_sha256": digest(target)}
    if only and set(only) - set(source):
        raise ValueError(f"{chapter}: unknown section IDs")
    write_json(records_path(language, chapter), records)


def translations(grouped, languages):
    localized = {"fr": grouped}
    work = []
    for language in languages:
        if language == "fr":
            continue
        localized[language] = {}
        paths = (ROOT / "translations" / language).glob("*")
        chapters = set(grouped) | {path.stem for path in paths if path.suffix in {".md", ".json"}}
        for chapter in sorted(chapters, key=lambda item: (item not in grouped, list(grouped).index(item) if item in grouped else item)):
            source = grouped.get(chapter, {})
            target = read_translation(translation_path(language, chapter))
            records = load_json(records_path(language, chapter), {})
            localized[language][chapter] = target
            statuses = defaultdict(list)
            for anchor in dict.fromkeys([*source, *target, *records]):
                status = translation_status(digest(source[anchor]) if anchor in source else None,
                                            digest(target[anchor]) if anchor in target else None,
                                            records.get(anchor))
                if anchor in source and anchor in target and signature(source[anchor]) != signature(target[anchor]):
                    status = "parity"
                if status != "current":
                    statuses[status].append(anchor)
            if not statuses and list(source) != list(target):
                statuses["order"] = list(target)
            if statuses:
                work.append((language, chapter, dict(statuses)))
    return localized, work


def yaml_front(data):
    # JSON scalar literals are compatible with the YAML front matter parser.
    return "---\n" + "".join(f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
                            for key, value in data.items()) + "---\n"


def stage(source, localized, registry, destination, baseurl):
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "site", destination, dirs_exist_ok=True)
    shutil.copyfile(ROOT / "LICENSE", destination / "LICENSE")
    aliases = alias_map(source, registry)
    locales = load_json(ROOT / "site" / "_data" / "locales.json")
    index = {}
    for language, chapters in localized.items():
        lang_path = destination / language
        lang_path.mkdir(exist_ok=True)
        index[language] = []
        for order, (chapter, sections) in enumerate(chapters.items()):
            title = next(HEADING.fullmatch(line)[2] for part in sections.values()
                         for line in part.splitlines()[:1] if HEADING.fullmatch(line))
            url = f"/{language}/" + ("" if chapter == "home" else chapter + "/")
            meta = locales[language]
            description = meta["description"] if chapter == "home" else meta["chapter_description"].format(chapter=title.replace("`", ""))
            metadata = dict(layout="guide", title=title, description=description, lang=language,
                            translation_key=chapter, permalink=url, nav_order=order, render_with_liquid=False)
            rendered = []
            toc = []
            for anchor, content in sections.items():
                before = content.splitlines(keepends=True)
                heading = HEADING.fullmatch(before[0].rstrip("\r\n")) if before else None
                if heading:
                    label = heading[2]
                    level = len(heading[1]) if anchor in {"chapter", "guide"} or len(heading[1]) > 1 else 5
                    before[0] = f"{'#' * level} {label}\n{{: #{anchor}}}\n"
                    toc.append({"id": anchor, "title": label, "level": level})
                linked = rewrite_links("".join(before), language, chapter, aliases[chapter], baseurl)
                rendered.append(render_prose(linked))
            index[language].append({"id": chapter, "title": title, "url": url, "toc": toc})
            (lang_path / f"{chapter}.md").write_text(yaml_front(metadata) + "".join(rendered), encoding="utf-8")
        (lang_path / "guide.md").write_text("".join(content for chapter in chapters.values() for content in chapter.values()),
                                           encoding="utf-8")
    write_json(destination / "_data" / "chapters.json", index)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["sync", "worklist", "record", "generate", "validate"])
    parser.add_argument("--lang", choices=LOCALES)
    parser.add_argument("--chapter")
    parser.add_argument("--sections", nargs="+")
    parser.add_argument("--destination", type=Path, default=ROOT / ".generated")
    parser.add_argument("--baseurl", default="/scala-agentic-engineering")
    args = parser.parse_args()
    source, registry_path, registry = sources()
    updated = allocate_ids(source, registry)
    if args.command == "sync":
        write_json(registry_path, updated)
        return 0
    if registry != updated:
        raise ValueError("New headings need stable IDs. Run python3 scripts/docs.py sync")
    grouped = group_source(source, registry)
    if args.command == "record":
        if args.lang not in set(LOCALES) - {"fr"} or args.chapter not in grouped:
            parser.error("record needs a target --lang and a valid --chapter")
        record(args.lang, args.chapter, grouped[args.chapter], not args.sections, args.sections)
        return 0
    if args.lang and args.command != "worklist":
        parser.error("--lang is supported by worklist and record")
    localized, work = translations(grouped, (args.lang,) if args.lang else LOCALES)
    for language, chapter, statuses in work:
        if not args.chapter or args.chapter == chapter:
            print(f"{language}/{chapter} " + " ".join(f"{status}={','.join(anchors)}" for status, anchors in statuses.items()))
    if args.command == "worklist":
        return 0
    if work:
        return 1
    if args.command == "generate":
        stage(source, localized, registry, args.destination, args.baseurl)
    print(f"{len(localized)} locales · {len(grouped) - 1} chapters · {len(source)} sections per locale")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        sys.exit(str(error))
