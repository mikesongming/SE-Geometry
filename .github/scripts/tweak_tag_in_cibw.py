#!/usr/bin/env python

import subprocess
from pathlib import Path

from versioningit import Versioningit


def main():
    project_dir = Path(__file__).parent.parent.parent

    vgit = Versioningit.from_project_dir(project_dir)
    report = vgit.run(write=False, fallback=True)
    if report.description.state == "exact":
        print(f"No tag tweaking needed: {report.base_version}")
        return
    else:
        print(
            "VCS state is %r; Tweaking tag for CI: %r -> %r"
            % (report.description.state, report.base_version, report.next_version)
        )
        subprocess.check_call(
            ["git", "tag", f"v{report.next_version}", "HEAD"], cwd=project_dir
        )


if __name__ == "__main__":
    main()
