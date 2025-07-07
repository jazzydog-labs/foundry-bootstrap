from __future__ import annotations

import os
import subprocess
import tarfile
from pathlib import Path


def test_install_pyenv_offline(tmp_path):
    repo_root = Path(__file__).resolve().parent.parent
    script = repo_root / "install" / "install_pyenv_linux.sh"

    # create minimal pyenv archive
    pyenv_src = tmp_path / "src" / "pyenv" / "bin"
    pyenv_src.mkdir(parents=True)
    fake = pyenv_src / "pyenv"
    fake.write_text("#!/bin/sh\necho pyenv")
    fake.chmod(0o755)

    archive = tmp_path / "pyenv.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(pyenv_src.parent, arcname="pyenv")

    env = {
        "HOME": str(tmp_path),
        "PYENV_ARCHIVE": str(archive),
        "PYENV_SKIP_DEPS": "1",
        "PATH": "/usr/bin:/bin",
    }

    subprocess.run(["bash", str(script)], check=True, env=env)

    assert (tmp_path / ".pyenv" / "bin" / "pyenv").exists()
