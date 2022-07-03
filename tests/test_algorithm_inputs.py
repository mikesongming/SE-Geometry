import pytest

from fseg.impl import Algorithm


class TestFSEGImplAlgorithm:
    @pytest.fixture(scope="function")
    def algorithm(self):
        return Algorithm()

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
        with pytest.raises(RuntimeError) as e:
            algorithm.calc_sun_position()

        assert "Tried to call pure virtual function" in str(e.value)

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

    def test_set_local_datetime_o1(self, algorithm, obs_time_t):
        algorithm.set_local_datetime(obs_time_t)
        assert algorithm.has_set_local_datetime()
        assert obs_time_t == algorithm.get_local_datetime()

    def test_set_local_datetime_o2(self, algorithm, obs_time_str, obs_time_t):
        algorithm.set_local_datetime(obs_time_str)
        assert algorithm.has_set_local_datetime()
        assert obs_time_t == algorithm.get_local_datetime()

    def test_set_local_datetime_o3(self, algorithm, obs_time_datetime, obs_time_t):
        algorithm.set_local_datetime(obs_time_datetime)
        assert algorithm.has_set_local_datetime()
        assert obs_time_t == algorithm.get_local_datetime()
