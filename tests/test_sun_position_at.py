from dataclasses import asdict

import pytest


class TestSEA_SunPositionAt:
    @pytest.fixture(scope="class", autouse=True)
    def set_observatory(self, sun_earth_analyzer, observatory):
        sun_earth_analyzer.observatory = observatory

    def test_str_input(
        self, sun_earth_analyzer, obs_time_str, obs_time_t, sun_position
    ):
        sp_result = sun_earth_analyzer.sun_position_at(obs_time_str, DEBUG=True)
        assert obs_time_t == sun_earth_analyzer._impl.get_local_datetime()
        assert asdict(sp_result) == pytest.approx(sun_position)

    def test_datetime_input(
        self, sun_earth_analyzer, obs_time_datetime, obs_time_t, sun_position
    ):
        sp_result = sun_earth_analyzer.sun_position_at(obs_time_datetime, DEBUG=True)
        assert obs_time_t == sun_earth_analyzer._impl.get_local_datetime()
        assert asdict(sp_result) == pytest.approx(sun_position)

    def test_ints_input(self, sun_earth_analyzer, obs_time_t, sun_position):
        sp_result = sun_earth_analyzer.sun_position_at(obs_time_t, DEBUG=True)
        assert obs_time_t == sun_earth_analyzer._impl.get_local_datetime()
        assert asdict(sp_result) == pytest.approx(sun_position)
