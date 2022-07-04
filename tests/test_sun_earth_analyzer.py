from dataclasses import asdict, astuple

import pytest

from fseg import Observatory, SunEarthAnalyzer
from fseg.impl import SPACalculator


class TestSunEarthAnalyzer:
    @pytest.fixture(scope="function")
    def sea(self):
        sea = SunEarthAnalyzer()
        yield sea

    @pytest.fixture(scope="function")
    def load_spa(self, sea):
        sea.algorithm = "SPA"

    def test_fail_wrong_algorithm(self, sea):
        with pytest.raises(ValueError, match="Unknown algorithm"):
            sea.algorithm = "NonExistent"

    def test_fail_algorithm_not_set(self, sea):
        assert sea.algorithm is None

        with pytest.raises(AttributeError, match=r"object has no attribute '_impl'"):
            sea._impl

    def test_load_spa_calculator(self, sea, load_spa):
        assert "SPA" == sea.algorithm
        assert isinstance(sea._impl, SPACalculator)

    def test_set_observatory(self, sea, load_spa, observatory):
        # initial not set
        assert not sea.has_set_observatory()
        assert sea.observatory is None

        # set with irrelevant key
        with pytest.raises(TypeError, match="an unexpected keyword argument"):
            sea.observatory = {"NonExistentKey": 1.0}
        assert not sea.has_set_observatory()
        assert sea.observatory is None

        # set with valid keys
        sea.observatory = observatory
        assert sea.has_set_observatory()
        assert observatory == asdict(sea.observatory)

        # change observatory
        toy_observatory = Observatory(*[1, 2, 3, 4])
        sea.observatory = toy_observatory
        assert [1, 2, 3, 4] == pytest.approx(astuple(sea.observatory)[:4])
        assert set([0]) == set(astuple(sea.observatory)[4:])
