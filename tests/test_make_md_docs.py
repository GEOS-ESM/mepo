import importlib.util
from pathlib import Path
import subprocess
from unittest.mock import Mock

import pytest
from mdutils.mdutils import MdUtils

spec = importlib.util.spec_from_file_location(
    "make_md_docs", Path(__file__).parents[1] / "docs" / "make_md_docs.py"
)
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)


def test_command_list_excludes_groups_and_private_modules(tmp_path):
    for name in ("__init__", "clone", "branch", "branch_list", "update-state"):
        (tmp_path / f"{name}.py").touch()
    assert docs.get_command_list(tmp_path) == ["branch list", "clone", "update-state"]


@pytest.mark.parametrize("options_heading", ["options", "optional arguments"])
def test_help_preserves_wrapped_usage_and_arguments(monkeypatch, options_heading):
    output = f"""usage: __main__.py clone [-h]
                         [URL]

Clone repositories.

positional arguments:
  URL  URL to clone

{options_heading}:
  -h, --help  show help
  --verbose  show retries
"""
    run = Mock(return_value=subprocess.CompletedProcess([], 0, stdout=output))
    monkeypatch.setattr(docs.sp, "run", run)
    markdown = MdUtils(file_name="unused")
    markdown.new_header(level=1, title="Commands")
    markdown.new_header(level=2, title="clone")
    docs.create_markdown_from_usage("clone", markdown)
    text = markdown.get_md_text()
    for expected in (
        "mepo clone",
        "[URL]",
        "Clone repositories.",
        "URL to clone",
        "--verbose",
    ):
        assert expected in text
    assert "__main__.py" not in text
    assert run.call_args.kwargs["check"] is True
    assert run.call_args.args[0][-2:] == ["clone", "--help"]


def test_help_failure_stops_generation(monkeypatch):
    run = Mock(side_effect=subprocess.CalledProcessError(2, "mepo"))
    monkeypatch.setattr(docs.sp, "run", run)
    with pytest.raises(subprocess.CalledProcessError):
        docs.create_markdown_from_usage("clone", MdUtils(file_name="unused"))
