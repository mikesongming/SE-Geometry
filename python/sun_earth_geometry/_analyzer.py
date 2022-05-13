from dataclasses import asdict
from datetime import datetime
from typing import Any, Tuple

from ._data import (
    OBS_TIME_T,
    Observatory,
    TopoCentricSunPositionResult,
    safely_from_dict,
)
from ._sun_earth_geometry import SPA_Analyzer


class SunEarthAnalyzer:
    def __init__(self, algorithm="SPA") -> None:
        self._algorithm = algorithm
        self._obs = Observatory(0.0, 0.0, 0.0, 0.0)
        self._load_algorithm()

    def _load_algorithm(self):
        if self._algorithm == "SPA":
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

    def has_set_observatory(self):
        return self._impl.has_set_observatory()

    def sun_position_at(
        self, dt: Any = None, DEBUG: bool = False, **kwargs
    ) -> Tuple[OBS_TIME_T, TopoCentricSunPositionResult]:
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
