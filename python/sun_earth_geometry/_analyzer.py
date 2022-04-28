from datetime import datetime
from dataclasses import asdict

from ._data import Observatory
from ._data import SunPositionResult

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
    
    def has_set_observatory(self):
        return self._impl.has_set_observatory()
    
    def sun_position_at(self, dt=None, DEBUG=False,
                        **kwargs) -> SunPositionResult:
        assert self.has_set_observatory(), "Observatory has not set"

        if isinstance(dt, str):
            dt = datetime.strptime("2003-10-17 12:30:30", "%Y-%m-%d %H:%M:%S")

        if isinstance(dt, datetime):
            sp = self._sun_position_at(dt.year, dt.month, dt.day,
                                       dt.hour, dt.minute, dt.second)
            if DEBUG:
                print("----------INPUT----------")
                print("Year:           %d" % dt.year)
                print("Month:          %d" % dt.month)    
                print("Day:            %d" % dt.day)      
                print("Hour:           %d" % dt.hour)     
                print("Minute:         %d" % dt.minute)   
                print("Second:         %d" % dt.second)
                print("Timezone:       %.6f" % self._obs.timezone)
                print("Longitude:      %.6f" % self._obs.longitude)
                print("Latitude:       %.6f" % self._obs.latitude)
                print("Elevation:      %.6f" % self._obs.elevation)
                print("Pressure:       %.6f" % self._obs.pressure)
                print("Temperature:    %.6f" % self._obs.temperature)
                print("Atmos_Refract:  %.6f" % self._obs.atmos_refract)   
                print("Delta T:        %.6f" % self._obs.delta_t)
                print("----------OUTPUT----------")
                print("Julian Day:    %.6f" % sp.julian_day)
                print("Zenith:        %.6f degrees" % sp.zenith)
                print("Azimuth:       %.6f degrees" % sp.azimuth)
            
            return sp
        else:
            raise ValueError(f"Invalid argument: {dt}")

    def _sun_position_at(self, year: int, month: int, day: int,
                         hour: int, minute: int, second: int):
        """
        directly call c++ library, when performance is critical
        """
        zenith, azimuth, julian_day = self._impl.calc_sun_position_at(
            year, month, day, hour, minute, second)

        return SunPositionResult(zenith, azimuth, julian_day)
    
    def __repr__(self) -> str:
        return f"SunEarthAnalyzer(algorithm={self._algorithm})"
