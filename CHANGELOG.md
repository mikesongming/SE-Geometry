# Release Notes

<!-- towncrier release notes start -->

## **v0.7.4** (2022-06-21)

### :bug: Bug Fixes

- [PR\#14](https://github.com/mikesongming/SE-Geometry/pull/14) tweak tag in
  build_sdist and build_wheel by CIBW


### :hammer_and_wrench: Maintenance

- [PR\#17](https://github.com/mikesongming/SE-Geometry/pull/17) directory
  refactoring


## **v0.7.2.1** (2022-06-21)

### :bug: Bug Fixes

-
  [0b1abcc](https://github.com/mikesongming/SE-Geometry/commit/0b1abccd7def53471d8ffd5fad8adaeeaf450e6f)
  call reused workflow publish_pypi.yml with inherited secrets


### :sparkles: Development Milestone

- [PR\#12](https://github.com/mikesongming/SE-Geometry/pull/12) support Linux
  on Ubuntu20.04 and MSVC on windows2019


### :hammer_and_wrench: Maintenance

-
  [6812935](https://github.com/mikesongming/SE-Geometry/commit/68129351c1860ae908acf86ccddbd4c4cd374016)
  GH checkout with ref and full history

- [PR\#15](https://github.com/mikesongming/SE-Geometry/pull/15) release
  triggered ci & publish


## **v0.6.0** (2022-06-18)

### :hammer_and_wrench: Maintenance

- [PR\#6](https://github.com/mikesongming/SE-Geometry/pull/6) customize github
  action workflows for CI


## **v0.5.0** (2022-05-25)

### :sparkles: Development Milestone

- [#1](https://github.com/mikesongming/SE-Geometry/issues/1)
[#2](https://github.com/mikesongming/SE-Geometry/issues/2)
[#3](https://github.com/mikesongming/SE-Geometry/issues/3)
A SunEarthAnalyzer API wrapping pybind11 C++ extension and CI/CD facilities
  > - SPA sun position algorithm implemented;
  > - Pytest empowered tests;
  > - pre-commit hooks, including mypy,isort,black,flake
  > - docs ready to gh-deploy by mkdocs, with the material theme
