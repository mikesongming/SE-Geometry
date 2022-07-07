# Release Notes

<!-- towncrier release notes start -->

## **v0.8.0** (2022-07-07)

### :bulb: API Changes

- [#24](https://github.com/mikesongming/SE-Geometry/issues/24) simplify python
  frontend api by refactoring c++ backend with pybind11-empowered virtual
  function overriding and methods overloading


### :memo: Documentation Improvements

- [#24](https://github.com/mikesongming/SE-Geometry/issues/24) update flow
  graph in dev-guid.md and docstring in _analyzer.py


### :hammer_and_wrench: Maintenance

- [PR\#26](https://github.com/mikesongming/SE-Geometry/pull/26) Introduce cmake
  module to fetch library pybind11 and date-tz; Modify setup.py to support
  c++17 on MacOSX >= 10.12;
  and Build windows version on Windows-2022 with manually downloaded tzdata


## **v0.7.6** (2022-06-28)

### :bug: Bug Fixes

- [30e2f2e](https://github.com/mikesongming/SE-Geometry/commit/30e2f2e) fix
  that collect_news changed last head commit


### :memo: Documentation Improvements

- [PR\#22](https://github.com/mikesongming/SE-Geometry/pull/22) Update
  Documents: user-guide/install.md dev-guide/


### :hammer_and_wrench: Maintenance

- [PR\#22](https://github.com/mikesongming/SE-Geometry/pull/22) Use
  [mermaid-js](https://mermaid-js.github.io/mermaid/) to draw UML graphs


## **v0.7.5** (2022-06-27)

### :rocket: Features

- [PR\#20](https://github.com/mikesongming/SE-Geometry/pull/20) Adopt Tox for
  local pytest & mkdocs

- [#18](https://github.com/mikesongming/SE-Geometry/issues/18) Add towncrier
  news collection


### :memo: Documentation Improvements

- [PR\#23](https://github.com/mikesongming/SE-Geometry/pull/23) Supplement
  change logs from v0.5.0 to v0.7.5


### :hammer_and_wrench: Maintenance

- [PR\#23](https://github.com/mikesongming/SE-Geometry/pull/23) Add workflow to
  build changelog and docs, then publish to GH Pages


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
