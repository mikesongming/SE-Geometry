import pytest

from fseg.impl import Algorithm, SPACalculator


@pytest.mark.skip(reason="Windows Stack Overflow")
class TestFSEGImplAlgorithm:
    @pytest.fixture(scope="function")
    def algorithm(self):
        return Algorithm()

    @pytest.fixture(scope="function")
    def spa_calculator(self):
        return SPACalculator()

    def test_name(self, algorithm):
        with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
            algorithm.name

    def test_spa_name(self, spa_calculator):
        assert "SPA" == spa_calculator.name

        with pytest.raises(AttributeError, match="can't set attribute"):
            spa_calculator.name = "Unknown"

    def test_static_attribute(self):
        assert [
            "longitude",
            "latitude",
            "elevation",
            "timezone",
            "delta_ut1",
            "delta_t",
            "pressure",
            "temperature",
            "atmos_refract",
        ] == Algorithm.OBS_FIELDS

    def test_pure_virtual_calculate_sun_position(self, algorithm):
        with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
            algorithm.calc_sun_position()

    def test_not_set_observatory_and_local_time(self, algorithm):
        assert not algorithm.has_set_observatory()
        assert not algorithm.has_set_local_datetime()

    def test_initial_observatory_and_local_time(self, algorithm):
        assert {} == algorithm.get_observatory()
        assert [0] * 6 == algorithm.get_local_datetime()

    def test_set_observatory_with_wrong_key_o1(self, algorithm):
        algorithm.set_observatory(NonExistentKey=1.0)
        assert not algorithm.has_set_observatory()
        assert {} == algorithm.get_observatory()

    def test_set_observatory_with_wrong_key_o2(self, algorithm):
        algorithm.set_observatory({"NonExistentKey": 1.0})
        assert not algorithm.has_set_observatory()
        assert {} == algorithm.get_observatory()

    def test_set_observatory_o1(self, algorithm, observatory):
        algorithm.set_observatory(
            longitude=2.0, latitude=3.0, elevation=100.0, NonExistentKey=1.0
        )
        assert algorithm.has_set_observatory()
        assert {
            "longitude": 2.0,
            "latitude": 3.0,
            "elevation": 100.0,
        } == algorithm.get_observatory()

        algorithm.set_observatory(**observatory)
        assert algorithm.has_set_observatory()
        assert observatory == algorithm.get_observatory()

    def test_set_observatory_o2(self, algorithm, observatory):
        algorithm.set_observatory(
            {
                "longitude": 2.0,
                "latitude": 3.0,
                "elevation": 100.0,
                "NonExistentKey": 1.0,
            }
        )
        assert algorithm.has_set_observatory()
        assert {
            "longitude": 2.0,
            "latitude": 3.0,
            "elevation": 100.0,
        } == algorithm.get_observatory()

        algorithm.set_observatory(observatory)
        assert algorithm.has_set_observatory()
        assert observatory == algorithm.get_observatory()

    def test_set_local_datetime_o1(self, algorithm, local_datetime):
        algorithm.set_local_datetime(local_datetime)
        assert algorithm.has_set_local_datetime()
        assert local_datetime == algorithm.get_local_datetime()

    def test_set_local_datetime_o2(self, algorithm, local_datetime_str, local_datetime):
        algorithm.set_local_datetime(local_datetime_str)
        assert algorithm.has_set_local_datetime()
        assert local_datetime == algorithm.get_local_datetime()

    def test_set_local_datetime_o2_fail(self, algorithm):
        local_date_time_str = "2019-13-05 12:30:90"
        with pytest.raises(ValueError, match="Mismatched datetime string"):
            algorithm.set_local_datetime(local_date_time_str)

    def test_set_local_datetime_o3(
        self, algorithm, local_datetime_datetime, local_datetime
    ):
        algorithm.set_local_datetime(local_datetime_datetime)
        assert algorithm.has_set_local_datetime()
        assert local_datetime == algorithm.get_local_datetime()
