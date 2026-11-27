import unittest

from scripts.docs import parse_source, rewrite_links, signature, translation_status, allocate_ids, render_prose


class DocumentationTest(unittest.TestCase):
    def test_chapters_ignore_headings_in_fences(self):
        text = "# Guide\n\n# 1. One\n\n````markdown\n```\n# 9. False\n````\n\n" \
               "~~~text\n# 8. Also false\n~~~\n\n# 1A. Real\n\n## Section\n"
        self.assertEqual([part.chapter for part in parse_source(text)], ["home", "ch-1", "ch-1a", "ch-1a"])
        self.assertEqual("".join(part.text for part in parse_source(text)), text)

    def test_quoted_text_fences_accept_localized_prose(self):
        source = "# Guide\n# 1. Chapter\n> ```text\n> # 2. Example\n> ```\n"
        self.assertEqual(len(parse_source(source)), 2)
        self.assertEqual(signature(source), signature(source.replace("Example", "Modified")))
        self.assertNotEqual(signature(source), signature(source.replace("> ```text", "```text").replace("> ```\n", "```\n")))

    def test_text_fences_preserve_technical_literals(self):
        fr = "```text\nBudget : 17 % ; vérifier `run` sur https://example.com/a\n```\n"
        en = "```text\nBudget: 17 %; check `run` at https://example.com/a\n```\n"
        self.assertEqual(signature(fr), signature(en))
        for altered in (en.replace("17", "18"), en.replace("run", "stop"), en.replace("/a", "/b")):
            self.assertNotEqual(signature(fr), signature(altered))

    def test_plaintext_fences_can_hold_literal_commands(self):
        source = "```plaintext\nsbt compile\n```\n"
        self.assertNotEqual(signature(source), signature(source.replace("compile", "test")))


    def test_wrapped_inline_code_retains_its_literal_content(self):
        self.assertEqual(signature("Run `command -a\n-b`."), signature("Lancer `command -a -b`."))
        self.assertNotEqual(signature("Run `command -a\n-b`."), signature("Lancer `command -a -c`."))

    def test_insertions_do_not_reassign_anchors(self):
        original = parse_source("# Guide\n# 1. One\n## Existing\n")
        registry = allocate_ids(original, {})
        edited = parse_source("# Guide\n# 1. One\n## New\n## Existing\n")
        updated = allocate_ids(edited, registry)
        self.assertEqual(updated["ch-1"]["headings"]["2:Existing"], "s-1")
        self.assertEqual(updated["ch-1"]["headings"]["2:New"], "s-2")

    def test_links_rewrite_across_pages_but_leave_code_and_urls(self):
        original = "[jump](guide.md#details) and `[x](#details)`\n\n~~~\n[x](#details)\n~~~\n"
        aliases = {"details": ("ch-2", "s-1")}
        result = rewrite_links(original, "fr", "ch-1", aliases, "/project")
        self.assertIn("[jump](/project/fr/ch-2/#s-1)", result)
        self.assertIn("`[x](#details)`", result)
        self.assertIn("~~~\n[x](#details)\n~~~", result)
        self.assertEqual(rewrite_links("[x](#details)", "de", "ch-2", aliases), "[x](#s-1)")
        self.assertEqual(rewrite_links("[x](https://example.com/#details)", "de", "ch-2", aliases),
                         "[x](https://example.com/#details)")
        self.assertEqual(rewrite_links("[ref]: #details", "de", "ch-1", aliases, "/project"), "[ref]: /project/de/ch-2/#s-1")

    def test_render_keeps_prose_pipes_out_of_tables(self):
        source = "Use **low | high** and https://example.net/a.\n---\n\n```text\nhttps://example.net/a\n```\n"
        rendered = render_prose(source)
        self.assertIn("**low \\| high** and <https://example.net/a>.\n\n---", rendered)
        self.assertIn("```text\nhttps://example.net/a\n```", rendered)

    def test_tracking(self):
        record = {"source_sha256": "source", "translation_sha256": "translation"}
        self.assertEqual(translation_status("source", "translation", record), "current")
        self.assertEqual(translation_status("updated", "translation", record), "stale")
        self.assertEqual(translation_status("source", "edited", record), "modified")
        self.assertEqual(translation_status("source", None, record), "missing")
        self.assertEqual(translation_status("source", "translation", None), "untracked")
        self.assertEqual(translation_status(None, "translation", record), "deleted")

    def test_parity_preserves_code_numbers_and_urls(self):
        fr = "## Chapitre\n\n* **Pour 17 %** https://example.com/a\n\n```bash\nexit 1\n```\n"
        en = "## Chapter\n\n* **For 17 %** https://example.com/a\n\n```bash\nexit 1\n```\n"
        self.assertEqual(signature(fr), signature(en))
        for altered in (en.replace("exit 1", "exit 2"), en.replace("17", "18"), en.replace("17 %", "17"),
                        en.replace("/a", "/b"), en.replace("* **", "**")):
            self.assertNotEqual(signature(fr), signature(altered))


if __name__ == "__main__":
    unittest.main()
