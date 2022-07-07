from dataclasses import asdict
from typing import Optional

from fseg._data import (
    DateTime_INPUT,
    LocalDateTime,
    Observatory,
    Observatory_INPUT,
    TopoCentricSunPositionResult,
)
from fseg.impl import registered_algorithms


class SunEarthAnalyzer(object):
    """
    Interface class for sun-earth-analysis

    Attributes:
        registered: map of algorithm name to its implementation class
        algorithm: name of algorithm
        observatory: relevant geological information of location
    """

    def __init__(self) -> None:
        self.registered = registered_algorithms

    @property
    def algorithm(self) -> Optional[str]:
        """
        unique name of algorithm

        Returns:
            Optional[str]: None if no algorithm loaded
        """
        if hasattr(self, "_impl"):
            return self._impl.name
        else:
            return None

    @algorithm.setter
    def algorithm(self, algorithm: str):
        if hasattr(self, "_impl"):
            del self._impl
        self._load_algorithm(algorithm)

    def _load_algorithm(self, _algorithm: str):
        algo_cls = self.registered.get(_algorithm)
        if algo_cls:
            self._impl = algo_cls()
        else:
            raise ValueError(f"Unknown algorithm: {_algorithm}")

    @property
    def observatory(self) -> Optional[Observatory]:
        """
        wrap c++ map<string, double> with dataclass Observatory

        Returns:
            Optional[Observatory]: None if observatory not set
        """
        if self.has_set_observatory():
            return Observatory(**self._impl.get_observatory())
        else:
            return None

    @observatory.setter
    def observatory(self, value: Observatory_INPUT):
        if hasattr(self, "_impl"):
            if isinstance(value, dict):
                value = Observatory(**value)
            self._impl.set_observatory(asdict(value))

    def has_set_observatory(self) -> bool:
        """
        check whether observatory is set for analyzer

        Returns:
            bool: True for set

        Examples:
            >>> sea = SunEarthAnalyzer()
            >>> sea.algorithm = "SPA"
            >>> sea.has_set_observatory()
            False
            >>> sea.sun_position_at([2020, 5, 13, 17, 15, 30])
            Traceback (most recent call last):
              ...
            RuntimeError: Observatory is unset

            >>> d = {'timezone': -7.0, 'longitude': -105.1786, 'latitude': 39.742476,
            ...      'elevation': 1830.14}
            >>> sea.observatory = d
            >>> sea.has_set_observatory()
            True
            >>> sea.observatory
            Observatory(longitude=-105.1786, latitude=39.742476, elevation=1830.14,
            timezone=-7.0, delta_ut1=0.0, delta_t=0.0, pressure=0.0, temperature=0.0,
            atmos_refract=0.0)
        """
        return hasattr(self, "_impl") and self._impl.has_set_observatory()

    def sun_position_at(self, dt: DateTime_INPUT) -> TopoCentricSunPositionResult:
        """
        API for calculating sun position at a time

        Args:
            dt (DateTime_INPUT): supports str, datetime and array format of observation
                time.

        Raises:
            ValueError: invalid inputs for observation time or
                failed at validation stage of the implemented algorithm

        Returns:
            sp (TopoCentricSunPositionResult): topocentric solar position with optional
                Julian day

        Examples:
            >>> sea = SunEarthAnalyzer()
            >>> sea.algorithm = "SPA"
            >>> sea.observatory = Observatory(
            ...     longitude=-105.1786, latitude=39.742476, elevation=1830.14,
            ...     timezone=-7.0, delta_ut1=0, delta_t=67,
            ...     pressure=820, temperature=11, atmos_refract=0.5667,
            ... )
            >>> sp = sea.sun_position_at("2003-10-17 12:30:30")
            >>> sp
            TopoCentricSunPositionResult(zenith=50.11162202402972,
            ... azimuth=194.34024051019162, julian_day=2452930.312847222)
            >>> sea._impl.get_local_datetime()
            [2003, 10, 17, 12, 30, 30]
        """
        self._impl.set_local_datetime(dt)
        return TopoCentricSunPositionResult(*self._impl.calc_sun_position())

    def __repr__(self) -> str:
        return f"SunEarthAnalyzer(algorithm={self.algorithm})"

    @staticmethod
    def print_sun_position_details(
        observatory: Observatory,
        local_datetime: LocalDateTime,
        sun_position: TopoCentricSunPositionResult,
    ):
        """
        print result in multiline format, for DEBUG

        Args:
            observatory (Observatory): _description_
            local_datetime (LocalDateTime): _description_
            sun_position (TopoCentricSunPositionResult): _description_
        """
        print("----------INPUT----------")
        print("Year:          %d" % local_datetime[0])
        print("Month:         %d" % local_datetime[1])
        print("Day:           %d" % local_datetime[2])
        print("Hour:          %d" % local_datetime[3])
        print("Minute:        %d" % local_datetime[4])
        print("Second:        %d" % local_datetime[5])
        print("Timezone:      %.6f" % observatory.timezone)
        print("Longitude:     %.6f" % observatory.longitude)
        print("Latitude:      %.6f" % observatory.latitude)
        print("Elevation:     %.6f" % observatory.elevation)
        print("Pressure:      %.6f" % observatory.pressure)
        print("Temperature:   %.6f" % observatory.temperature)
        print("Atmos_Refract: %.6f" % observatory.atmos_refract)
        print("Delta T:       %.6f" % observatory.delta_t)
        print("----------OUTPUT----------")
        if sun_position.julian_day:
            print("Julian Day:    %.6f" % sun_position.julian_day)
        print("Zenith:        %.6f degrees" % sun_position.zenith)
        print("Azimuth:       %.6f degrees" % sun_position.azimuth)
