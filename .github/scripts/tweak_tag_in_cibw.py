#!/usr/bin/env python

import subprocess
from pathlib import Path

import versioningit


def main():
    project_dir = Path(__file__).parent.parent.parent

    subprocess.check_call(
        ["git", "describe", "--dirty", "--long", "--always", "--tags", "--match", "v*"],
        cwd=project_dir,
    )

    rev = versioningit.get_version(project_dir)
    next_rev = versioningit.get_next_version(project_dir)

    if rev == next_rev:
        print(f"No tag tweaking needed: v{rev}")
        return

    print(f"Tweaking tag for CI: {rev} -> {next_rev}")
    subprocess.check_call("git", "tag", f"v{next_rev}", "HEAD", cwd=project_dir)
    subprocess.check_call(
        ["git", "describe", "--dirty", "--long", "--always", "--tags", "--match", "v*"],
        cwd=project_dir,
    )


if __name__ == "__main__":
    main()
