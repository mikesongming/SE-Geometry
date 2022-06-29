import pytest

from fseg import SunEarthAnalyzer


class TestSunEarthAnalyzer:
    @pytest.fixture(scope="function")
    def sea(self):
        sea = SunEarthAnalyzer()
        yield sea

    @pytest.mark.xfail(reason="Algorithm is empty", raises=ValueError)
    def test_fail_empty_algorithm(self, sea):
        sea.algorithm = ""

    @pytest.mark.xfail(reason="Algorithm is invalid", raises=ValueError)
    def test_fail_wrong_algorithm(self, sea):
        sea.algorithm = "NonExistent"

    @pytest.mark.xfail(reason="No algorithm is set", raises=AttributeError)
    def test_fail_algorithm_not_set(self, sea):
        assert sea._impl is None
        sea.has_set_observatory()
