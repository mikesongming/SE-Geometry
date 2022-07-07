# Developer's Guide

## Local Development Procedure

1. Install [Anaconda](https://www.anaconda.com/) on System
2. Install [CMake](https://cmake.org) on System
3. Install C++/C Compiler on System, w.r.t. [supported platforms](../index.md#supported-platforms)
4. Checkout issue related branch from [Github](https://github.com/mikesongming/SE-Geometry)
5. Prepare Python environment, either by
```
pip install -r requirements-dev.txt
```
or
```
pip install tox && tox -e dev
```
6. Add `pre-commit` git hooks
```
python -m pre_commit install
```
7. Browse and edit source code as your wish, [VSCode](https://code.visualstudio.com/) recommened as the IDE
8. Broadcast your work using [towncrier](https://towncrier.readthedocs.io/en/latest/) by:
```
towncrier create {source}.{type} --edit
```
where {type} is one of:
> - feature: for new features
> - api: for API changes
> - bug: for bug fixes
> - maint: for maintenance and ci related
> - dev: for breakthrough changes/milestone
> - doc: for documentation changes
> - author: for contributor names

and where the {source} part of the filename is:
> - 42 when the change is described in issue 42
> - PR42 when the change has been implemented in pull request 42, and there is no associated issue
> - Cabcdef when the change has been implemented in changeset abcdef, and there is no associated issue or pull request.
> - username for contributors (author extention). It should be the username part of their commits’ email address.

## Library Design

<!--
empowered by [Mermaid-Js](https://mermaid-js.github.io/mermaid/)
-->
### 1. Flowchart

``` mermaid
flowchart LR
    i1((Observatory))
    i2((Local Datatime))
    c1[SunEarthAnalyzer]
    a1[py::Algorithm]
    a2[py::SPACalculator]
    b1[Algorithm]
    b2[SPACalculator]
    d1[(C implementation of<br>SPA algorithm)]

    i1---c1
    i2---c1

    Py<===>|pybind11|Cpp

    subgraph Frontend
        c1--->Py
        subgraph Py
            direction TB
            a1-->a2
        end
    end

    subgraph Backend
        Cpp--->d1

        subgraph Cpp
            direction TB
            b1-->b2
        end
    end
```

### 2. Sequence Diagram

``` mermaid
sequenceDiagram
    participant SunEarthAnalyzer
    participant SPACalculator
    participant SPA
    SunEarthAnalyzer ->>+ SPACalculator: load algorithm
    SPACalculator -->>- SunEarthAnalyzer: calculator

    SunEarthAnalyzer ->> SPACalculator: set observatory
    SunEarthAnalyzer ->> SPACalculator: set local datetime

    SunEarthAnalyzer ->>+ SPACalculator: sun position ?
    % break when observatory not set
    %     SPACalculator -->> SunEarthAnalyzer: RuntimeError
    % end
    SPACalculator -->>+ SPA: calculate sun position at ?
    % break when validate_inputs fails
    %     SPA-->SPACalculator: error code
    % end
    SPA -->> SPA: spa calcluate
    SPA -->>- SPACalculator: spa_data
    SPACalculator -->>- SunEarthAnalyzer: TopoCentricSunPositionResult
```

### 3. Class Diagram

``` mermaid
classDiagram
    SunEarthAnalyzer "1" --> "0..1" Algorithm: load algorithm
    SunEarthAnalyzer "1" --> "0..1" Observatory: set observatory
    SunEarthAnalyzer --> TopoCentricSunPositionResult: sun position at
    Algorithm <|-- SPACalculator
    Algorithm <|-- SG2_Calculator
    Algorithm <|-- Other_Algorithm
    class SunEarthAnalyzer {
        +algorithm: string
        +observatory: Observatory
        +registered: dict
        -_impl: Algorithm
        +has_set_observatory()
        +sun_position_at(local_datetime)
        -_load_algorithm()
    }
    class Algorithm {
        -_observatory_set: bool = false
        -_local_datetime_set: bool = false
        -_observatory: map<string, double>
        -_local_datetime: array<int>
        + static OBS_FIELDS: vector<string>
        +has_set_observatory()
        +get_observatory()
        +set_observatory(...)
        +has_set_local_datetime()
        +get_local_datetime()
        +set_local_datetime(...)
        +virtual: name()
        +virtual: calc_sun_position()
    }
    <<interface>> Algorithm
    class SPACalculator {
        -_spa: spa_data

    }
    class SG2_Calculator {
        TODO
    }
    class Observatory {
        +longitude: float
        +latitude: float
        +elevation: float
        +timezone: float
        +delta_ut1: float = 0
        +delta_t: float = 0
        +pressure: float = 0
        +temperature: float = 0
        +atmos_refract: float = 0
    }
    class TopoCentricSunPositionResult {
        +zenith: float
        +azimuth: float
        +julian_day: float = None
    }
```

## How to add algorithm

1. Add an sub-class of `Algorithm`, implementing two methods: `name` and `calc_sun_position`

2. Add a [pybind11 trampoline class](https://pybind11.readthedocs.io/en/stable/advanced/classes.html#overriding-virtual-functions-in-python) for the new algorithm class for automatic downcasting

3. Bind the algorithm to python in `src/cpp/main.cpp`
```cpp
    py::class_<SPACalculator, Algorithm, PySPACaculator>(m, "SPACalculator")
        .def(py::init<>())
        .def_property_readonly("name", &SPACalculator::name)
        .def("calc_sun_position", &SPACalculator::calc_sun_position);
```
4. Register the algorithm in `src/python/fseg/impl/__init__.py`
```py
registered_algorithms = {
    "SPA": SPACalculator,
}
```
## Tests by Pytest

Currently, only Python code is tested by pytest. You are welcome to incorporate C++ tests.

Testing via [tox](https://tox.readthedocs.io/):
```
tox -r -e dev -- -s -v
```

## Documentation Preivew

Docs is managed by [Material for Mkdocs](https://squidfunk.github.io/mkdocs-material/). Preview docs by:
```
tox -r -e docs
```
