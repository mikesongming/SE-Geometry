from pathlib import Path

import pytest
import tomli

from fseg import SunEarthAnalyzer

TEST_ROOT = Path(__file__).parent
with open(TEST_ROOT.joinpath("case_data.toml"), "rb") as f:
    case_data = tomli.load(f)["case_data"]


@pytest.fixture(scope="module", params=["SPA"])
def sun_earth_analyzer(request):
    sea = SunEarthAnalyzer()
    sea.algorithm = request.param
    yield sea


@pytest.fixture(scope="module", params=case_data["sun_position_at"])
def sun_position_case(request):
    input = request.param["input"]
    output = request.param["output"]

    yield (input["observatory"], input["time"], output)


@pytest.fixture(scope="module")
def observatory(sun_position_case):
    return sun_position_case[0]


@pytest.fixture(scope="module")
def obs_time_datetime(sun_position_case):
    return sun_position_case[1]["datetime"]


@pytest.fixture(scope="module")
def obs_time_str(sun_position_case):
    return sun_position_case[1]["string"]


@pytest.fixture(scope="module")
def obs_time_t(sun_position_case):
    return sun_position_case[1]["array"]


@pytest.fixture(scope="module")
def sun_position(sun_position_case):
    return sun_position_case[2]
