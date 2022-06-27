
FSEG is implemented as a python package with a pybind11 extension.
Currently, the project is at _Pre-Alpha_ stage, and you can install FSEG
either from PYPI or from source. Later, installation with Anaconda is  more recommended.

## with PIP

```sh
pip install FSEG
```

## with GIT
<!-- <small>recommended</small> { #with-git data-toc-label="with git" } -->
- pre-requirements

It is required that [cmake](https://cmake.org) and C++ compiler installed beforehand.
[Anaconda](https://www.anaconda.com/) is also needed to manager python envs.

For example, on MacOSX with [Homebrew](https://brew.sh/):
```sh
brew install anaconda
brew install cmake
```

- clone source code by:
```sh
git clone https://github.com/mikesongming/SE-Geometry.git
```

- build and install

After changing to the source directory, it is recommended to use [PEP517](https://peps.python.org/pep-0517)-compatible build-system to package the wheel:
```sh
python -m build -w
```

If successful, install the wheel by pip:
```sh
pip install dist/fseg-${ver}-${plat_name}_${arch}.whl
```
