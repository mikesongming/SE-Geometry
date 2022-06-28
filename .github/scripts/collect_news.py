#!/usr/bin/env python

import subprocess
from pathlib import Path

import towncrier.build
from versioningit import Versioningit


def main():
    project_dir = Path(__file__).parent.parent.parent

    # add all changes into index
    subprocess.check_call(["git", "add", "-A", "."], cwd=project_dir)

    vgit = Versioningit.from_project_dir(project_dir)
    report = vgit.run(write=False, fallback=True)
    if report.description.state == "exact":
        print(f"current state is exact: {report.version}")
        # call towncrier build with report.version
        towncrier.build.__main(
            False, project_dir, None, None, report.version, None, True
        )
        subprocess.check_call(
            ["git", "commit", "-m", f"changelog {report.version}"], cwd=project_dir
        )
    else:
        print(
            "VCS state is %r; using next-version for changelog: %r"
            % (report.description.state, report.next_version)
        )
        subprocess.check_call(
            ["git", "commit", "--allow-empty", "-m", "temp commit with news"],
            cwd=project_dir,
        )
        towncrier.build.__main(
            False, project_dir, None, None, report.next_version, None, True
        )
        subprocess.check_call(["git", "reset", "--soft", "HEAD~"], cwd=project_dir)
        subprocess.check_call(["git", "add", "-A", "."], cwd=project_dir)
        subprocess.check_call(
            ["git", "commit", "-m", f"changelog {report.next_version}"], cwd=project_dir
        )


if __name__ == "__main__":
    main()
