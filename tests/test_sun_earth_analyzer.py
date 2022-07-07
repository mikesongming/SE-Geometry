from dataclasses import asdict, astuple

import pytest

from fseg import Observatory, SunEarthAnalyzer
from fseg.impl import SPACalculator
from tests.conftest import Foo


class TestSunEarthAnalyzer:
    @pytest.fixture(scope="function")
    def sea(self):
        sea = SunEarthAnalyzer()
        yield sea

    @pytest.fixture(scope="function")
    def load_spa(self, sea):
        sea.algorithm = "SPA"

    @pytest.fixture(scope="function")
    def register_foo(self, sea):
        sea.registered["Foo"] = Foo
        yield
        sea.registered.pop("Foo", None)

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
        assert observatory == pytest.approx(asdict(sea.observatory))

        # change observatory
        toy_observatory = Observatory(*[1, 2, 3, 4])
        sea.observatory = toy_observatory
        assert [1, 2, 3, 4] == pytest.approx(astuple(sea.observatory)[:4])
        assert set([0]) == set(astuple(sea.observatory)[4:])

    def test_change_algorithm(
        self, sea, load_spa, register_foo, observatory, local_datetime
    ):
        sea.observatory = observatory
        assert "SPA" == sea.algorithm
        assert sea.has_set_observatory()

        sea.algorithm = "Foo"
        assert "Foo" == sea.algorithm
        assert "Foo" in str(sea)
        assert not sea.has_set_observatory()

        sea.observatory = observatory
        sp = sea.sun_position_at(local_datetime)
        assert observatory == pytest.approx(asdict(sea.observatory))
        assert local_datetime == pytest.approx(sea._impl.get_local_datetime())
        SunEarthAnalyzer.print_sun_position_details(
            sea.observatory, sea._impl.get_local_datetime(), sp
        )
