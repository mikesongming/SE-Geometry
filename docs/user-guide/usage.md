First, import the library:

```py
import fseg
print(fseg.__version__)
```

!!! note

    Since there is no system time-zone data on **Windows**,
    it is necessary to download [IANA](https://www.iana.org/time-zones)
    tzdata for the library date-tz.

    ```bash
    mkdir $HOME/tzdata
    cd $HOME/tzdata
    curl "https://data.iana.org/time-zones/releases/tzdata2022a.tar.gz" | tar xvz
    curl "https://raw.githubusercontent.com/unicode-org/cldr/main/common/supplemental/windowsZones.xml"
    ```

    If `curl` failed with `connection refused`, manually download the `windowsZones.xml` file in browser.

    <font color="red">Windows version was forgone at v0.8.0 </font>

## sun position at

1. Instantialize an `analyzer`, and bound to an _algorithm_, for example _"SPA"_:

    ```py
    from fseg import SunEarthAnalyzer

    sea = SunEarthAnalyzer()
    sea.algorithm="SPA"
    ```

2. Set the observatory using _kwargs_ arguments:

    ```py
    d = {'timezone': -7.0, 'longitude': -105.1786, 'latitude': 39.742476,
         'elevation': 1830.14}
    sea.observatory = d
    ```

    Without setting observatory, a runtime error will be raised when calling for calculation:
    ```py
    >>> sea.has_set_observatory()
    False
    >>> sea.sun_position_at([2020, 5, 13, 17, 15, 30])
    Traceback (most recent call last):
      ...
    RuntimeError: Observatory is unset
    ```

3. Call the backend algorithm to calculate sun position at the give _time_:
    ```py
    >>> sp = sea.sun_position_at("2003-10-17 12:30:30")
    >>> sp
    TopoCentricSunPositionResult(zenith=50.11162202402972,
    ... azimuth=194.34024051019162, julian_day=2452930.312847222)
    ```
Other type of arguments like `List[int]` and `datetime.datetime` are also supported, see [reference](https://mikesongming.github.io/SE-Geometry/reference/SunEarthAnalyzer/#fseg._analyzer.SunEarthAnalyzer.sun_position_at) for details.

<!-- ##  sun path

##  sunlight analysis
-->
