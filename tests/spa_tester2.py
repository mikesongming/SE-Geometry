from sun_earth_geometry import SunEarthAnalyzer

if __name__ == "__main__":
    sea = SunEarthAnalyzer()
    sea.set_observatory(
        timezone=-7.0,
        delta_ut1=0,
        delta_t=67,
        longitude=-105.1786,
        latitude=39.742476,
        elevation=1830.14,
        pressure=820,
        temperature=11,
        atmos_refract=0.5667,
    )
    # print(sea._obs)

    sp = sea.sun_position_at("2003-10-17 12:30:30", DEBUG=True)

    from datetime import datetime

    dt = datetime.strptime("2003-10-17 12:30:30", "%Y-%m-%d %H:%M:%S")
    sp = sea.sun_position_at(dt, DEBUG=True)
    sp = sea.sun_position_at(
        year=2003, month=10, day=17, hour=12, minute=30, second=30, DEBUG=True
    )
    sp = sea.sun_position_at(
        year=2003, month=10, day=17, hour=12, minute=30, second=30, DEBUG=True
    )
    # print(sp)

    # sp2 = sea.sun_path_at(year=2003, month=10, day=17, DEBUG=True)
    # sp2 = sea.sun_path_at("2003-10-17", DEBUG=True)
    # sp2 = sea.sun_path_at(datetime.strptime("2003-10-17", "%Y-%m-%d"), DEBUG=True)
