import subprocess as sp

def run(cmd, output=None, status=None):
    result = sp.run(
        cmd,
        stdout = sp.PIPE,
        stderr = sp.PIPE,
        universal_newlines = True # result byte sequence -> string
    )

    if status:
        return result.returncode
    elif result.returncode != 0:
        print(result.stderr)
        result.check_returncode()

    if output:
        return result.stdout + result.stderr
