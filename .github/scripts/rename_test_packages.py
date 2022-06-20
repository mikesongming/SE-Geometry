#!/usr/bin/env python

"""
REV='0.7.1.post2+ga1b438c'
N_REV='0.7.2'

for pkg in `ls dist/* | grep ${REV}`;
do
    n_pkg=`echo $pkg | awk -F "${REV}" "{print $1,${N_REV},$2}"`
    echo $pkg '->' $n_pkg
done
"""
import os
from pathlib import Path

rev = os.environ.get("REV")
next_rev = os.environ.get("N_REV")
assert rev is not None, "env.REV is not set!"
assert next_rev is not None, "env.N_REV is not set!"

_script = Path(__file__)


def rename_pkg(pkg):
    n_name = pkg.name.replace(rev, next_rev)
    n_pkg = pkg.parent.joinpath(n_name)
    print(n_pkg)
    pkg.rename(n_pkg)


def main():
    project_root = _script.parent.parent.parent
    dist = project_root.joinpath("dist")

    for pkg in dist.glob("*.tar.gz"):
        rename_pkg(pkg)

    for pkg in dist.glob("*.whl"):
        rename_pkg(pkg)


if __name__ == "__main__":
    main()
