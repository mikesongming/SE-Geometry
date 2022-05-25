from datetime import datetime

import pytest

from fseg import SunEarthAnalyzer

from .case_data import sun_position_data


@pytest.fixture(scope="module", params=["SPA"])
def sun_earth_analyzer(request):
    sea = SunEarthAnalyzer(algorithm=request.param)
    yield sea


@pytest.fixture(scope="module", params=range(len(sun_position_data)))
def sun_position_case(request):
    case_id = request.param
    case_data = sun_position_data[case_id]
    case_input = case_data["input"]
    case_output = case_data["output"]
    obs = case_input["observatory"]
    obs_time_t = tuple(
        case_input["time"].get(k)
        for k in ["year", "month", "day", "hour", "minute", "second"]
    )
    sp_result = case_output

    yield (obs, obs_time_t, sp_result)


@pytest.fixture(scope="module")
def observatory(sun_position_case):
    return sun_position_case[0]


@pytest.fixture(scope="module")
def obs_time_str(obs_time_datetime):
    return obs_time_datetime.strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(scope="module")
def obs_time_datetime(obs_time_t):
    return datetime(*obs_time_t)


@pytest.fixture(scope="module")
def obs_time_t(sun_position_case):
    return sun_position_case[1]


@pytest.fixture(scope="module")
def sun_position(sun_position_case):
    return sun_position_case[2]
