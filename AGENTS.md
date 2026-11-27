# Documentation

- Edit the source content in `guide.md`. Preserve the existing anchors in `translations/sections.json`.
- Use the glossary for sections listed by `python3 scripts/docs.py worklist` and update their manifests with `scripts/docs.py record`.
- Run `scripts/build` before merging. Keep `_site/` out of version control.
