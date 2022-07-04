from dataclasses import asdict
from typing import Any, Optional, Union

from fseg._data import Observatory, TopoCentricSunPositionResult
from fseg.impl import registered_algorithms


class SunEarthAnalyzer(object):
    """
    Interface class for sun-earth-analysis
    """

    def __init__(self) -> None:
        self.registered = registered_algorithms

    @property
    def algorithm(self) -> Optional[str]:
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
        if _algorithm in self.registered:
            self._impl = self.registered[_algorithm]()
        else:
            raise ValueError(f"Unknown algorithm: {_algorithm}")

    @property
    def observatory(self) -> Optional[Observatory]:
        if self.has_set_observatory():
            return Observatory(**self._impl.get_observatory())
        else:
            return None

    @observatory.setter
    def observatory(self, value: Union[Observatory, dict]):
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
            >>> sea.has_set_observatory()
            False
            >>> sea.sun_position_at(2020,5,13,17,15,30)
            Traceback (most recent call last):
              ...
            RuntimeError: Observatory has not set

            >>> d = {'timezone': -7.0, 'longitude': -105.1786, 'latitude': 39.742476,
            ...      'elevation': 1830.14, 'foo': 100.0}
            >>> sea.set_observatory(**d)
            >>> sea.has_set_observatory()
            True
        """
        return hasattr(self, "_impl") and self._impl.has_set_observatory()

    def sun_position_at(
        self, dt: Any = None, DEBUG: bool = False
    ) -> TopoCentricSunPositionResult:
        """
        API for calculating sun position at a time

        Args:
            dt (Any, optional): supports str and datetime format of observation
                time. Defaults to None, when kwargs of (year, month, day, hour,
                minute, second) must be given.
            DEBUG (bool, optional): when set, print result in multiline format.
                Defaults to False.

        Raises:
            ValueError: invalid inputs for observation time or
                failed at validation stage of the implemented algorithm

        Returns:
            (dt,sp) (Tuple[OBS_TIME_T, TopoCentricSunPositionResult]):
                dt (year,month,day,hour,minute,second): parsed observation time
                sp: topocentric solar position with julian day

        Examples:
            >>> sea = SunEarthAnalyzer()
            >>> sea.set_observatory(
            ...     longitude=-105.1786, latitude=39.742476, elevation=1830.14,
            ...     timezone=-7.0, delta_ut1=0, delta_t=67,
            ...     pressure=820, temperature=11, atmos_refract=0.5667,
            ... )
            >>> dt, sp = sea.sun_position_at("2003-10-17 12:30:30")
            >>> dt
            (2003, 10, 17, 12, 30, 30)
            >>> sp
            TopoCentricSunPositionResult(zenith=50.11162202402972,
            ... azimuth=194.34024051019162, julian_day=2452930.312847222)
        """
        self._impl.set_local_datetime(dt)
        obs_time_t = self._impl.get_local_datetime()
        obs = Observatory(**self._impl.get_observatory())
        sp = TopoCentricSunPositionResult(*self._impl.calc_sun_position())

        if DEBUG:
            print("----------INPUT----------")
            print("Year:           %d" % obs_time_t[0])
            print("Month:          %d" % obs_time_t[1])
            print("Day:            %d" % obs_time_t[2])
            print("Hour:           %d" % obs_time_t[3])
            print("Minute:         %d" % obs_time_t[4])
            print("Second:         %d" % obs_time_t[5])
            print("Timezone:       %.6f" % obs.timezone)
            print("Longitude:      %.6f" % obs.longitude)
            print("Latitude:       %.6f" % obs.latitude)
            print("Elevation:      %.6f" % obs.elevation)
            print("Pressure:       %.6f" % obs.pressure)
            print("Temperature:    %.6f" % obs.temperature)
            print("Atmos_Refract:  %.6f" % obs.atmos_refract)
            print("Delta T:        %.6f" % obs.delta_t)
            print("----------OUTPUT----------")
            if sp.julian_day:
                print("Julian Day:    %.6f" % sp.julian_day)
            print("Zenith:        %.6f degrees" % sp.zenith)
            print("Azimuth:       %.6f degrees" % sp.azimuth)

        return sp

    def __repr__(self) -> str:
        return f"SunEarthAnalyzer(algorithm={self.algorithm})"
