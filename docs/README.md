# Command reference

From a development checkout with `uv sync` completed, run:

```sh
uv run python docs/make_md_docs.py
```

This generates `Mepo-Commands.md` in the current directory from the checkout's
command help, including unreleased changes. Review it and copy it into the
separately cloned `mepo.wiki` repository. Commit and publish wiki changes
separately from the main repository.

Regenerate this page whenever commands or options change. Update the wiki's
Configuration and workflow pages separately when behavior changes.
