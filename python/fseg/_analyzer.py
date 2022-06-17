from dataclasses import asdict
from datetime import datetime
from typing import Any, Tuple

from ._data import (
    OBS_TIME_T,
    Observatory,
    TopoCentricSunPositionResult,
    safely_from_dict,
)
from ._fseg import SPA_Analyzer


class SunEarthAnalyzer(object):
    """
    Interface class for sun-earth-analysis

    Args:
        algorithm (str): currently supports 'SPA'; Defaults to 'SPA'
    """

    def __init__(self, algorithm: str = "SPA") -> None:
        self._algorithm = algorithm
        self._obs = Observatory(0.0, 0.0, 0.0, 0.0)
        self._load_algorithm()

    def _load_algorithm(self):
        if self._algorithm.upper() == "SPA":
            self._impl = SPA_Analyzer()
        else:
            raise ValueError(f"Unknown algorithm {self._algorithm}")

    def set_observatory(self, **kwargs) -> None:
        obs_keys = vars(self._obs)
        for k, v in kwargs.items():
            if k in obs_keys:
                setattr(self._obs, k, v)

        self._impl.set_observatory(**asdict(self._obs))

    def get_observatory(self) -> Observatory:
        if self.has_set_observatory():
            return safely_from_dict(self._impl.get_observatory(), Observatory)
        else:
            return self._obs

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
        return self._impl.has_set_observatory()

    def sun_position_at(
        self, dt: Any = None, DEBUG: bool = False, **kwargs
    ) -> Tuple[OBS_TIME_T, TopoCentricSunPositionResult]:
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
        try:
            if dt is None:
                _year, _month = int(kwargs["year"]), int(kwargs["month"])
                _day, _hour = int(kwargs["day"]), int(kwargs["hour"])
                _minute, _second = int(kwargs["minute"]), int(kwargs["second"])
            else:
                if isinstance(dt, str):
                    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

                if isinstance(dt, datetime):
                    _year, _month, _day = dt.year, dt.month, dt.day
                    _hour, _minute, _second = dt.hour, dt.minute, dt.second
                else:
                    raise TypeError(f"Invalid type for dt: {type(dt)}")
        except Exception:
            raise ValueError(f"Invalid argument: dt={dt}, {kwargs}")

        sp = self._sun_position_at(_year, _month, _day, _hour, _minute, _second)

        if DEBUG:
            obs = self.get_observatory()
            print("----------INPUT----------")
            print("Year:           %d" % _year)
            print("Month:          %d" % _month)
            print("Day:            %d" % _day)
            print("Hour:           %d" % _hour)
            print("Minute:         %d" % _minute)
            print("Second:         %d" % _second)
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

        dt = (_year, _month, _day, _hour, _minute, _second)
        return dt, sp

    def _sun_position_at(
        self, year: int, month: int, day: int, hour: int, minute: int, second: int
    ) -> TopoCentricSunPositionResult:
        """
        directly call c++ library, when performance is critical
        """
        zenith, azimuth, julian_day = self._impl.calc_sun_position_at(
            year, month, day, hour, minute, second
        )

        return TopoCentricSunPositionResult(zenith, azimuth, julian_day)

    def __repr__(self) -> str:
        return f"SunEarthAnalyzer(algorithm={self._algorithm})"
