from dataclasses import asdict
from datetime import datetime

import pytest

from sun_earth_geometry import (
    Observatory,
    SunEarthAnalyzer,
    TopoCentricSunPositionResult,
)


@pytest.fixture
def observatory():
    obs = Observatory(
        longitude=-105.1786,
        latitude=39.742476,
        elevation=1830.14,
        timezone=-7.0,
        delta_ut1=0,
        delta_t=67,
        pressure=820,
        temperature=11,
        atmos_refract=0.5667,
    )
    return asdict(obs)


@pytest.fixture
def analyzer(observatory):
    analyzer = SunEarthAnalyzer()
    analyzer.set_observatory(**observatory)
    return analyzer


@pytest.fixture
def obs_time_str():
    return "2003-10-17 12:30:30"


@pytest.fixture
def obs_time_datetime(obs_time_str):
    return datetime.strptime(obs_time_str, "%Y-%m-%d %H:%M:%S")


@pytest.fixture
def obs_time_t(obs_time_datetime):
    return (2003, 10, 17, 12, 30, 30)


@pytest.fixture
def sun_position():
    return TopoCentricSunPositionResult(
        julian_day=2452930.312847, zenith=50.111622, azimuth=194.340241
    )
