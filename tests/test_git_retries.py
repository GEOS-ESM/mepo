import configparser
import subprocess as sp
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

from mepo.command import develop
from mepo.git import GitRepository
from mepo.utilities import mepoconfig, shellcmd
from mepo.utilities.exceptions import RepoAlreadyClonedError


TIMEOUT = (
    "ssh: connect to host github.com port 22: Connection timed out\n"
    "fatal: Could not read from remote repository.\n"
)


@pytest.fixture
def runner(monkeypatch):
    monkeypatch.setattr(mepoconfig, "config", configparser.ConfigParser())
    run = Mock()
    monkeypatch.setattr(shellcmd.sp, "run", run)
    monkeypatch.setattr(shellcmd.time, "sleep", Mock())
    return run


def result(code=0, stdout="", stderr=""):
    return sp.CompletedProcess(["git"], code, stdout, stderr)


@pytest.mark.parametrize("operation", ["pull", "fetch", "checkout", "diff", "status"])
def test_transport_retry_preserves_repo_and_output(runner, tmp_path, capsys, operation):
    tracked = tmp_path / "local-work"
    tracked.write_text("keep me")
    runner.side_effect = [
        result(1, stderr=TIMEOUT),
        result(stdout="ok\n", stderr="note"),
    ]
    repo = GitRepository("git@github.com:example/repo.git", str(tmp_path))
    if operation == "checkout":
        assert repo.checkout("develop") is None
        assert "--force" not in runner.call_args.args[0]
    elif operation == "fetch":
        args = SimpleNamespace(all=True, prune=True, tags=True, force=False)
        assert repo.fetch(args) == "ok\nnote"
    elif operation == "diff":
        args = SimpleNamespace(
            ignore_permissions=False,
            name_only=False,
            name_status=False,
            staged=False,
            ignore_space_change=False,
        )
        assert repo.run_diff(args) == "ok\nnote"
    elif operation == "status":
        assert repo.check_status() == "ok\nnote"
    else:
        assert repo.pull() == "ok\nnote"
    assert runner.call_count == 2
    shellcmd.time.sleep.assert_called_once_with(5)
    assert tracked.read_text() == "keep me"
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "error",
    [
        "error: pathspec 'no-such-tag' did not match any file(s) known to git",
        "error: Your local changes would be overwritten by checkout",
        "CONFLICT (content): Merge conflict in file.txt",
        "Permission denied (publickey).\nfatal: Could not read from remote repository.",
        "fatal: repository 'https://github.com/example/missing.git/' not found",
    ],
)
def test_non_transport_errors_fail_immediately(runner, tmp_path, capsys, error):
    runner.return_value = result(1, stderr=error)
    repo = GitRepository("origin", str(tmp_path))
    with pytest.raises(sp.CalledProcessError):
        repo.checkout("no-such-tag")
    runner.assert_called_once()
    shellcmd.time.sleep.assert_not_called()
    assert error in capsys.readouterr().out


def test_attempt_limit_and_final_error(runner, capsys):
    runner.return_value = result(1, stderr=TIMEOUT)
    with pytest.raises(sp.CalledProcessError):
        shellcmd.run(["git", "pull"], retry=True)
    assert runner.call_count == 4
    assert shellcmd.time.sleep.call_args_list == [call(5), call(10), call(15)]
    assert capsys.readouterr().out.count(TIMEOUT) == 1


@pytest.mark.parametrize("attempts", ["0", "1", "2"])
def test_attempts_setting(runner, attempts):
    mepoconfig.config.read_dict({"git": {"attempts": attempts}})
    runner.return_value = result(1, stderr=TIMEOUT)
    assert shellcmd.run(["git", "cat-file"], status=True, retry=True) == 1
    assert runner.call_count == max(1, int(attempts))


def test_verbose_and_stdout_mode(runner, capsys):
    mepoconfig.config.read_dict({"git": {"verbose": "true"}})
    runner.side_effect = [
        result(1, stderr=TIMEOUT),
        result(stdout="hash", stderr="note"),
    ]
    assert shellcmd.run(["git", "ls-remote"], stdout=True, retry=True) == "hash"
    output = capsys.readouterr().out
    assert TIMEOUT in output
    assert "retry 1/3 in 5s" in output


def test_clone_settings_do_not_control_retries(runner, capsys):
    mepoconfig.config.read_dict({"clone": {"attempts": "1", "verbose": "true"}})
    runner.return_value = result(1, stderr=TIMEOUT)
    assert shellcmd.run(["git", "fetch"], status=True, retry=True) == 1
    assert runner.call_count == 4
    assert capsys.readouterr().out == ""


def test_explicit_verbose_overrides_config(runner, capsys):
    mepoconfig.config.read_dict({"git": {"verbose": "false"}})
    runner.side_effect = [result(1, stderr=TIMEOUT), result()]
    shellcmd.run_with_retries(["git", "clone"], verbose=True)
    assert "retry 1/3 in 5s" in capsys.readouterr().out


def test_invalid_attempts_rejected(runner):
    mepoconfig.config.read_dict({"git": {"attempts": "invalid"}})
    with pytest.raises(ValueError):
        shellcmd.run(["git", "fetch"], retry=True)
    runner.assert_not_called()


@pytest.mark.parametrize("custom_ssh", [None, "ssh -p 443 -o ConnectTimeout=10"])
def test_ssh_timeout_is_scoped_and_respects_user(runner, monkeypatch, custom_ssh):
    monkeypatch.delenv("GIT_SSH_COMMAND", raising=False)
    if custom_ssh:
        monkeypatch.setenv("GIT_SSH_COMMAND", custom_ssh)
    runner.return_value = result()
    shellcmd.run(["git", "pull"], retry=True)
    assert runner.call_args.kwargs["env"]["GIT_SSH_COMMAND"] == (
        custom_ssh or "ssh -o ConnectTimeout=20"
    )
    assert shellcmd.os.environ.get("GIT_SSH_COMMAND") == custom_ssh


def test_clone_only_cleans_new_directory(runner, tmp_path):
    path = tmp_path / "clone"

    def run(*args, **kwargs):
        assert not path.exists()
        path.mkdir()
        if runner.call_count == 1:
            (path / "partial").write_text("incomplete")
            return result(1, stderr=TIMEOUT)
        return result()

    runner.side_effect = run
    repo = GitRepository("origin", str(path))
    assert repo.clone() == 1
    assert path.is_dir()
    (path / "local-work").write_text("keep me")
    with pytest.raises(RepoAlreadyClonedError):
        repo.clone()
    assert runner.call_count == 2
    assert (path / "local-work").read_text() == "keep me"


def test_clone_checkout_retries_without_cleanup(runner, tmp_path):
    runner.side_effect = [result(), result(1, stderr=TIMEOUT), result()]
    repo = GitRepository("origin", str(tmp_path))
    assert repo.clone(version="main") == 1
    assert "--force" in runner.call_args.args[0]
    assert tmp_path.is_dir()


@pytest.mark.parametrize(
    "operation", ["push", "pop_stash", "apply_stash", "commit_files"]
)
def test_stateful_commands_do_not_retry(runner, tmp_path, operation):
    runner.return_value = result(1, stderr=TIMEOUT)
    repo = GitRepository("origin", str(tmp_path))
    with pytest.raises(sp.CalledProcessError):
        method = getattr(repo, operation)
        method("message") if operation == "commit_files" else method()
    runner.assert_called_once()
    shellcmd.time.sleep.assert_not_called()


@pytest.mark.parametrize(
    "error",
    [
        "fatal: repository not found",
        "Permission denied (publickey).\nfatal: Could not read from remote repository.",
    ],
)
def test_clone_non_transport_error_does_not_retry(runner, tmp_path, error):
    runner.return_value = result(1, stderr=error)
    with pytest.raises(sp.CalledProcessError):
        GitRepository("origin", str(tmp_path / "new")).clone()
    runner.assert_called_once()
    shellcmd.time.sleep.assert_not_called()


def test_missing_post_clone_ref_does_not_retry(runner, tmp_path):
    runner.side_effect = [
        result(),
        result(
            1, stderr="error: pathspec 'missing' did not match any file(s) known to git"
        ),
    ]
    with pytest.raises(sp.CalledProcessError):
        GitRepository("origin", str(tmp_path)).clone(version="missing")
    assert runner.call_count == 2
    shellcmd.time.sleep.assert_not_called()


@pytest.mark.parametrize(
    "error",
    [
        "ssh: Could not resolve hostname github.com: Temporary failure in name resolution",
        "fatal: unable to access 'https://github.com/example/repo': Could not resolve host: github.com",
        "fatal: unable to access 'https://github.com/example/repo': Failed to connect to github.com port 443",
        "fatal: unable to access 'https://github.com/example/repo': Recv failure: Connection reset by peer",
    ],
)
def test_other_transport_errors_retry(runner, error):
    runner.side_effect = [result(1, stderr=error), result()]
    shellcmd.run(["git", "fetch"], retry=True)
    assert runner.call_count == 2


def test_develop_retries_pull(runner, monkeypatch, tmp_path):
    comp = SimpleNamespace(
        name="component",
        remote="origin",
        local=str(tmp_path),
        develop="develop",
        recurse_submodules=None,
    )
    monkeypatch.setattr(develop.MepoState, "read_state", lambda: [comp])
    runner.side_effect = [result(), result(1, stderr=TIMEOUT), result()]
    develop.run(SimpleNamespace(comp_name=[comp.name], quiet=True))
    assert [args.args[0][-1] for args in runner.call_args_list] == [
        "develop",
        "pull",
        "pull",
    ]
    shellcmd.time.sleep.assert_called_once_with(5)


def test_real_git_missing_ref_preserves_work(monkeypatch, tmp_path):
    monkeypatch.setattr(mepoconfig, "config", configparser.ConfigParser())
    sp.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    sp.run(
        [
            "git",
            "-C",
            str(tmp_path),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "--quiet",
            "--allow-empty",
            "-m",
            "initial",
        ],
        check=True,
    )
    local_work = tmp_path / "local-work"
    local_work.write_text("keep me")
    run = Mock(wraps=sp.run)
    monkeypatch.setattr(shellcmd.sp, "run", run)
    sleep = Mock()
    monkeypatch.setattr(shellcmd.time, "sleep", sleep)
    with pytest.raises(sp.CalledProcessError):
        GitRepository("origin", str(tmp_path)).checkout("no-such-ref")
    run.assert_called_once()
    sleep.assert_not_called()
    assert local_work.read_text() == "keep me"
