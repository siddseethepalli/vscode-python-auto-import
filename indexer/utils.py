import contextlib
import os
from pathlib import Path
import subprocess
from typing import Generator


def get_base_dir(path: str) -> str | None:
    p = Path(path).absolute()

    while str(p) != "/":
        # Root of a git repository
        if (p / ".git").exists():
            return str(p)

        # Root of the python part of a Django project
        if (p / "manage.py").exists():
            return str(p)

        # Root of a python project
        if (p / "requirements.txt").exists():
            return str(p)

        p = p.parent

    return None


def list_all_target_files():
    targets = [
        t.decode()
        for t in subprocess.check_output(
            "( git status --short . | grep '^?' | cut -d\\  -f2- && git ls-files .) | grep '\\.py$' | sort -u",
            shell=True,
        ).splitlines()
    ]
    return targets


@contextlib.contextmanager
def change_directory(tmpdir: str) -> Generator[None, None, None]:
    curdir = os.getcwd()
    try:
        os.chdir(tmpdir)
        yield
    finally:
        os.chdir(curdir)
