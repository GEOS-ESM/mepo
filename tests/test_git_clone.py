from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from mepo.command.clone import clone_components
from mepo.git import GitRepository
from mepo.utilities import shellcmd


@pytest.mark.parametrize("partial", [None, "blobless", "treeless"])
@pytest.mark.parametrize("recurse", [None, True])
def test_clone_filters_submodules_only_with_filter_and_recursion(
    monkeypatch, tmp_path, partial, recurse
):
    run = Mock(return_value=(SimpleNamespace(returncode=0), 0))
    monkeypatch.setattr(shellcmd, "run_with_retries", run)
    repo = GitRepository("origin", str(tmp_path / "clone"))

    assert repo.clone(version="main", partial=partial, recurse=recurse) == 0

    clone_cmd = run.call_args_list[0].args[0]
    assert ("--recurse-submodules" in clone_cmd) == bool(recurse)
    assert ("--also-filter-submodules" in clone_cmd) == (
        partial is not None and bool(recurse)
    )
    filters = {
        None: None,
        "blobless": "--filter=blob:none",
        "treeless": "--filter=tree:0",
    }
    assert [arg for arg in clone_cmd if arg.startswith("--filter=")] == (
        [filters[partial]] if partial is not None else []
    )
    checkout_cmd = run.call_args_list[1].args[0]
    assert "--also-filter-submodules" not in checkout_cmd
    assert ("--recurse-submodules" in checkout_cmd) == bool(recurse)


@pytest.mark.parametrize(
    "partial, blobless, filtered",
    [
        (None, True, True),
        ("blobless", None, True),
        ("treeless", None, False),
        ("treeless", True, True),
    ],
)
def test_component_clone_submodule_filter_policy(
    monkeypatch, tmp_path, partial, blobless, filtered
):
    run = Mock(return_value=(SimpleNamespace(returncode=0), 0))
    monkeypatch.setattr(shellcmd, "run_with_retries", run)
    comp = SimpleNamespace(
        name="component",
        fixture=False,
        recurse_submodules=True,
        blobless=blobless,
        version=SimpleNamespace(name="main", type="b"),
        remote="origin",
        local=str(tmp_path / "clone"),
        sparse=None,
    )

    clone_components([comp], partial)

    clone_cmd = run.call_args_list[0].args[0]
    assert ("--filter=blob:none" in clone_cmd) == filtered
    assert ("--also-filter-submodules" in clone_cmd) == filtered
    assert "--filter=tree:0" not in clone_cmd
