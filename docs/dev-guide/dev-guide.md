# Developer's Guide

## Local Development Procedure

1. Install [Anaconda](https://www.anaconda.com/) on System
2. Install [CMake](https://cmake.org) on System
3. Install C++/C Compiler on System, w.r.t. [supported platforms](https://mikesongming.github.io/SE-Geometry/#supported-platforms)
4. Checkout issue related branch from [Github](https://github.com/mikesongming/SE-Geometry)
5. Prepare Python environment, either by
```
pip install -r requirements-dev.txt
```
or
```
pip install tox && tox -e dev
```
6. Browse and edit source code as your wish, [VSCode](https://code.visualstudio.com/) recommened as the IDE
7. Broadcast your work using [towncrier](https://towncrier.readthedocs.io/en/latest/) by:
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
    i2((OBS_TIME_T))
    c1[SunEarthAnalyzer]
    a1[py::Algorithm]
    a2[py::SPA_Calculator]
    b1[Algorithm]
    b2[SPA_Calculator]
    d1[(C implementation of<br>SPA algorithm)]

    i1---c1
    i2---c1

    Py<===>|pybind11|CPP

    subgraph Python
        c1--->Py
        subgraph Py
            direction TB
            a1-->a2
        end
    end

    subgraph CPP
        direction TB
        b1-->b2
        b2--->d1
    end
```

### 2. Sequence Diagram

``` mermaid
sequenceDiagram
    participant SunEarthAnalyzer
    participant SPA_Calculator
    participant SPA
    SunEarthAnalyzer ->>+ SPA_Calculator: load algorithm
    SPA_Calculator -->>- SunEarthAnalyzer: calculator

    SunEarthAnalyzer ->> SPA_Calculator: set observatory

    SunEarthAnalyzer ->>+ SPA_Calculator: sun position at ?
    % break when observatory not set
    %     SPA_Calculator -->> SunEarthAnalyzer: RuntimeError
    % end
    SPA_Calculator -->>+ SPA: calculate sun position at ?
    % break when validate_inputs fails
    %     SPA-->SPA_Calculator: error code
    % end
    SPA -->> SPA: spa calcluate
    SPA -->>- SPA_Calculator: spa_data
    SPA_Calculator -->>- SunEarthAnalyzer: TopoCentricSunPositionResult
```

### 3. Class Diagram

``` mermaid
classDiagram
    SunEarthAnalyzer "1" --> "0..1" Algorithm: load algorithm
    SunEarthAnalyzer "1" --> "0..1" Observatory: set observatory
    SunEarthAnalyzer --> TopoCentricSunPositionResult: sun position at
    Algorithm <|-- SPA_Calculator
    Algorithm <|-- SG2_Calculator
    Algorithm <|-- Other_Algorithm
    TopoCentricSunPositionResult --> OBS_TIME_T
    class SunEarthAnalyzer {
        +String algorithm
        +Observatory observatory
        -Algorithm _impl
        +has_set_observatory()
        +sun_position_at(obs_time: OBS_TIME_T)
        -_load_algorithm()
    }
    class Algorithm {
        -_observatory_set: bool = false
        +virtual: get_observatory()
        +virtual: set_observatory(kwargs)
        +virtual: calc_sun_position_at(year,month,day,hour,minute,second)
        +has_set_observatory()
    }
    <<interface>> Algorithm
    class SPA_Calculator {
        -_observatory: map[string, double]
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

    class OBS_TIME_T {
        +year: int
        +month: int
        +day: int
        +hour: int
        +minute: int
        +second: int
    }
    class TopoCentricSunPositionResult {
        +zenith: float
        +azimuth: float
        +julian_day: float = None
        +obs_time: OBS_TIME_T = None
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
