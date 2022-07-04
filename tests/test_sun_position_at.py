from dataclasses import asdict

import pytest

from fseg import SunEarthAnalyzer


class TestSEA_SunPositionAt:
    @pytest.fixture(scope="class", autouse=True)
    def set_observatory(self, sun_earth_analyzer, observatory):
        sun_earth_analyzer.observatory = observatory

    def test_str_input(
        self, sun_earth_analyzer, local_datetime_str, local_datetime, sun_position
    ):
        sp_result = sun_earth_analyzer.sun_position_at(local_datetime_str)
        assert local_datetime == sun_earth_analyzer._impl.get_local_datetime()
        assert asdict(sp_result) == pytest.approx(sun_position)

    def test_datetime_input(
        self, sun_earth_analyzer, local_datetime_datetime, local_datetime, sun_position
    ):
        sp_result = sun_earth_analyzer.sun_position_at(local_datetime_datetime)
        assert local_datetime == sun_earth_analyzer._impl.get_local_datetime()
        assert asdict(sp_result) == pytest.approx(sun_position)

    def test_ints_input(self, sun_earth_analyzer, local_datetime, sun_position):
        sp_result = sun_earth_analyzer.sun_position_at(local_datetime)
        SunEarthAnalyzer.print_sun_position_details(
            sun_earth_analyzer.observatory, local_datetime, sp_result
        )
        assert local_datetime == sun_earth_analyzer._impl.get_local_datetime()
        assert asdict(sp_result) == pytest.approx(sun_position)
