from dataclasses import asdict

import pytest


@pytest.mark.skip
class TestSEA_SunPositionAt:
    @pytest.fixture(scope="class", autouse=True)
    def set_observatory(self, sun_earth_analyzer, observatory):
        sun_earth_analyzer.set_observatory(**observatory)

    def test_str_input(
        self, sun_earth_analyzer, obs_time_str, obs_time_t, sun_position
    ):
        dt, sp_result = sun_earth_analyzer.sun_position_at(obs_time_str, DEBUG=True)
        assert dt == obs_time_t
        assert asdict(sp_result) == pytest.approx(sun_position)

    def test_datetime_input(
        self, sun_earth_analyzer, obs_time_datetime, obs_time_t, sun_position
    ):
        dt, sp_result = sun_earth_analyzer.sun_position_at(
            obs_time_datetime, DEBUG=True
        )
        assert dt == obs_time_t
        assert asdict(sp_result) == pytest.approx(sun_position)

    def test_ints_input(self, sun_earth_analyzer, obs_time_t, sun_position):
        dt, sp_result = sun_earth_analyzer.sun_position_at(
            year=obs_time_t[0],
            month=obs_time_t[1],
            day=obs_time_t[2],
            hour=obs_time_t[3],
            minute=obs_time_t[4],
            second=obs_time_t[5],
            DEBUG=True,
        )
        assert dt == obs_time_t
        assert asdict(sp_result) == pytest.approx(sun_position)
