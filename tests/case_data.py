sun_position_data = [
    # test case 1, from "spa_tester.c"
    {
        "input": {
            "observatory": {
                "longitude": -105.1786,
                "latitude": 39.742476,
                "elevation": 1830.14,
                "timezone": -7.0,
                "delta_ut1": 0,
                "delta_t": 67,
                "pressure": 820,
                "temperature": 11,
                "atmos_refract": 0.5667,
            },
            "time": {
                "year": 2003,
                "month": 10,
                "day": 17,
                "hour": 12,
                "minute": 30,
                "second": 30,
            },
        },
        "output": {
            "julian_day": 2452930.312847,
            "zenith": 50.111622,
            "azimuth": 194.340241,
        },
    },
]
