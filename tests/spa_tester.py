# from datetime import datetime

import warnings
from typing import Dict, Union

from sun_earth_geometry import _sun_earth_geometry

# spd = sp.SPData()

# spd.year          = 2003
# spd.month         = 10
# spd.day           = 17
# spd.hour          = 12
# spd.minute        = 30
# spd.second        = 30
# spd.timezone      = -7.0
# spd.delta_ut1     = 0
# spd.delta_t       = 67
# spd.longitude     = -105.1786
# spd.latitude      = 39.742476
# spd.elevation     = 1830.14
# spd.pressure      = 820
# spd.temperature   = 11
# spd.atmos_refract = 0.5667

# # sp.spa_calculate(spd, False)
# sp.spa_calculate(spd, True)

if __name__ == "__main__":
    if _sun_earth_geometry.__version__ >= "0.3":
        warnings.warn(
            "SunPositionAnalysis is deprecated; use SunEarthAnalyzer.",
            DeprecationWarning,
        )
    else:
        from sun_earth_geometry._sun_earth_geometry import SunPositionAnalysis

        # spa = SunPositionAnalysis(year=2003, month=10, day=17,
        #     hour=12, minute=30, second=30,
        #     timezone=-7.0, delta_ut1=0, delta_t=67,
        #     longitude=-105.1786, latitude=39.742476, elevation=1830.14,
        #     pressure=820, temperature=11, atmos_refract=0.5667)
        input2 = {
            "timezone": -7.0,
            "delta_ut1": 0,
            "delta_t": 67,
            "longitude": -105.1786,
            "latitude": 39.742476,
            "elevation": 1830.14,
            "pressure": 820,
            "temperature": 11,
            "atmos_refract": 0.5667,
        }
        input_full: Dict[str, Union[int, float]] = {
            "year": 2003,
            "month": 10,
            "day": 17,
            "hour": 12,
            "minute": 30,
            "second": 30,
            **input2,
        }
        # spa = SunPositionAnalysis(**input_full)
        # spa = SunPositionAnalysis(year=2003, month=10, day=17, **input2)
        spa = SunPositionAnalysis("2003-10-17 12:30:30", **input2)
        # spa = SunPositionAnalysis(
        #     datetime.strptime("2003-10-17 12:30:30", "%Y-%m-%d %H:%M:%S"),
        #     **input2)

        print("----------INPUT----------")
        spa.print_input()
        spa()  # spa(with_sun_rts=False)
        # spa(with_sun_rts=True)
        print("----------OUTPUT----------")
        spa.print_output()
