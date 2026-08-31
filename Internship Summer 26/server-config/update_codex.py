import os
import shutil
import stat
import tarfile
import tempfile
import urllib.request


URL = "https://github.com/openai/codex/releases/download/rust-v0.147.0/codex-x86_64-unknown-linux-musl.tar.gz"


def find_codex_binary(root: str) -> str:
    for current_root, _, files in os.walk(root):
        if "codex" in files:
            return os.path.join(current_root, "codex")
        for filename in files:
            if filename.startswith("codex-"):
                return os.path.join(current_root, filename)
    raise FileNotFoundError("Could not find the codex binary in the extracted archive")


def main() -> None:
    os.makedirs(os.path.expanduser("~/bin"), exist_ok=True)

    fd, archive = tempfile.mkstemp(suffix=".tar.gz")
    os.close(fd)

    try:
        urllib.request.urlretrieve(URL, archive)

        tmpdir = tempfile.mkdtemp()
        try:
            with tarfile.open(archive, "r:gz") as tf:
                tf.extractall(tmpdir)

            src = find_codex_binary(tmpdir)
            dst = os.path.expanduser("~/bin/codex")
            shutil.copy2(src, dst)
            os.chmod(
                dst,
                os.stat(dst).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
            )
            print(dst)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
    finally:
        if os.path.exists(archive):
            os.remove(archive)


if __name__ == "__main__":
    main()
