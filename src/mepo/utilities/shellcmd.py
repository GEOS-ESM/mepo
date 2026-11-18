import os
import shutil
import subprocess as sp
import time

from . import mepoconfig


def run_with_retries(cmd, verbose=False, cleanup=None):
    """Return (result, retry count); cleanup is only for a new clone's directory."""
    config = mepoconfig.config
    attempts = max(1, config.getint("git", "attempts", fallback=6))
    verbose = verbose or config.getboolean("git", "verbose", fallback=False)
    env = os.environ.copy()
    env.setdefault("GIT_SSH_COMMAND", "ssh -o ConnectTimeout=20")
    for attempt in range(1, attempts + 1):
        result = sp.run(
            cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, env=env
        )
        # shortcut: English transport diagnostics only; extend for other Git/SSH locales as needed.
        transient = any(
            message in result.stderr.lower()
            for message in (
                "connection timed out",
                "connection timeout",
                "operation timed out",
                "connection reset",
                "connection refused",
                "network is unreachable",
                "no route to host",
                "temporary failure in name resolution",
                "could not resolve host",
                "failed to connect to",
                "couldn't connect to server",
                "remote end hung up unexpectedly",
                "recv failure",
            )
        )
        if result.returncode == 0 or not transient or attempt == attempts:
            return result, attempt - 1
        delay = 5 * attempt
        if verbose:
            print(result.stderr)
            print(f"git failed ({cmd}), retry {attempt}/{attempts - 1} in {delay}s")
        if cleanup is not None:
            shutil.rmtree(cleanup, ignore_errors=True)
        time.sleep(delay)


def run(cmd, output=None, stdout=None, status=None, retry=False):
    if retry:
        result, _ = run_with_retries(cmd)
    else:
        result = sp.run(
            cmd,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            universal_newlines=True,  # result byte sequence -> string
        )

    if status:
        return result.returncode
    elif result.returncode != 0:
        print(result.stderr)
        result.check_returncode()

    if stdout:
        return result.stdout
    if output:
        return result.stdout + result.stderr
