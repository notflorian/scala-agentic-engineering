# Scala Agentic Engineering

A documentation site built with Jekyll and Just the Docs from the [French source guide](guide.md). The public home page opens the English version. Chapter URLs follow `/<lang>/ch-<number>/`, for example `/en/ch-7a/`. The six language prefixes are `en`, `fr`, `es`, `pt`, `it`, and `de`.

## Local preview

Install the Ruby version in [`.ruby-version`](.ruby-version), the Bundler version in [`Gemfile.lock`](Gemfile.lock), Python 3.10 or later, and Node.js 20 or later.

```sh
bundle install
PAGES_URL=http://localhost:8000 PAGES_BASEURL='' scripts/build
python3 -m http.server 8000 --directory _site
```

Open the [local preview](http://localhost:8000). Run `scripts/build` again after editing. The command runs the tests, checks translations, builds with `JEKYLL_ENV=production`, generates search indexes from the HTML, and validates the rendered pages. It defaults to the project's GitHub Pages URL when `PAGES_URL` and `PAGES_BASEURL` are unset.

## Site presentation

The guide layout and its includes render the handbook from the generated chapter catalog. Update chapter groups and homepage topic destinations in [`site/_data/navigation.json`](site/_data/navigation.json), and add interface copy in all six languages in [`site/_data/locales.json`](site/_data/locales.json). The build checks group order, topic destinations, pagination, and localized controls.

The site uses its own navigation, search dialog, heading permalinks, and code-copy controls. Just the Docs provides the theme’s reset, table styles, and HTML table wrappers. The guide stylesheet defines the color tokens and Rouge highlighting for both appearances. The search indexes are still generated from the rendered editorial content and fetched on demand.

## Update the guide

1. Edit [`guide.md`](guide.md). Numbered H1 headings that follow the chapter sequence start new pages. Subheadings and fenced blocks stay in their chapter.
2. Run `python3 scripts/docs.py sync` if you added headings. Before renaming a heading, update its key in [`translations/sections.json`](translations/sections.json) and keep its value. When removing a heading, keep the entry to reserve its anchor.
3. Run `python3 scripts/docs.py worklist`. Each line lists the language, chapter, status, and section IDs to address. Use filters such as `--lang de --chapter ch-7a` to scope an assignment.
4. Update `translations/<lang>/<chapter>.md`. Keep the `<!-- section: ID -->` markers in order and remove deleted sections. Use the [translation glossary](translations/GLOSSARY.md) and check revised passages against the French source.
5. Record the reviewed sections with `python3 scripts/docs.py record --lang de --chapter ch-7a --sections chapter s-1`. Omit `--sections` to record the entire chapter and remove manifest entries for sections already deleted from the translated file. If an entire chapter is removed, delete its Markdown file and manifest in each translation.
6. Run `scripts/build` before submitting the change. The initial translation drafts were generated locally and need technical and linguistic review.

### Identifiers and manifests

`translations/sections.json` maps each French heading and its level to a stable anchor within its chapter. `next` stores the next available number. The main heading anchors are `guide` and `chapter`. Subsections use IDs such as `s-1` and `s-2`, shared across all six languages.

Alongside each translated chapter, a JSON manifest maps every section ID to `source_sha256` and `translation_sha256`. Each SHA-256 hash covers the UTF-8 bytes of the corresponding section, excluding its marker. Validation flags missing, deleted, outdated, unrecorded, out-of-order, and structurally mismatched sections. It compares fenced blocks, inline code, link destinations, numeric values, headings, lists, blockquotes, and tables. Translation and review take place outside CI.

Use a `text` fence for prose, including prompts, diagrams, and checklists. Translate its contents while preserving formatting, inline literals, links, and numbers. Use a language-specific fence for code and commands, or `plaintext` for literal unhighlighted snippets. Keep those blocks identical in all languages.

### Split translation work between Codex and Claude Code

Start from a branch with a shared version of `guide.md` and assign distinct language and chapter pairs. Give each session its section IDs from the worklist, the glossary, and the manifest conventions. The following commands create separate worktrees.

```sh
git worktree add -b docs/es-ch-7a ../scala-codex
git worktree add -b docs/de-ch-7a ../scala-claude
```

Open Codex in `../scala-codex` and Claude Code in `../scala-claude`. Ask each session to edit only its Markdown file and manifest, then check its assignment with `worklist --lang … --chapter …`. Integrate both branches and run the full validation on the combined result.

## Publish to GitHub Pages

Before publishing, confirm that the content, attributions, and licenses permit public distribution. In the repository settings, open **Pages** and choose **GitHub Actions** as the source. After changes land on `main`, the workflow builds and validates the site, then deploys the artifact to the `github-pages` environment. Pull requests run validation only. The generated HTML stays outside the repository.

Configure a custom domain under **Settings → Pages**. The workflow reads the active Pages origin and path prefix. [GitHub Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
