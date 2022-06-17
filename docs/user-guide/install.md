# Getting started

FSEG is implemented as a python package with a pybind11 extension.
Currently, you can only install FSEG from source since the project is at
"Pre-Alpha" stage. Later, installation with pip is  more recommended.

## Installation

### pre-requirements

Since we need to compile backend extensions before installing the package,
it is required that [cmake](https://cmake.org) and [pybind11](https://pybind11.readthedocs.io/) installed beforehand.

- MacOSX with [Homebrew](https://brew.sh/)
    ```sh
    brew install cmake pybind11
    ```

### with GIT
<!-- <small>recommended</small> { #with-git data-toc-label="with git" } -->

Source code of FSEG can be cloned from [Github](https://github.com) by:
```sh
git clone https://github.com/mikesongming/SE-Geometry.git
```

After changing to the source directory, it is recommended to use [PEP517](https://peps.python.org/pep-0517)-compatible build-system to package the wheel:
```sh
python -m build
```

If successful, we can install the wheel by pip:
```sh
pip install dist/fseg-${ver}-${plat_name}_${arch}.whl
```

### with PIP <small>to be setup</small> { #with-pip data-toc-label="with pip" }

Ideally, you can install with:

```sh
pip install FSEG
```
