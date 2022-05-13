from dataclasses import asdict

import pytest


def test_str_input_spa(analyzer, obs_time_str, obs_time_t, sun_position):
    dt, sp_result = analyzer.sun_position_at(obs_time_str)
    assert dt == obs_time_t
    assert asdict(sp_result) == pytest.approx(asdict(sun_position))


def test_datetime_input_spa(analyzer, obs_time_datetime, obs_time_t, sun_position):
    dt, sp_result = analyzer.sun_position_at(obs_time_datetime)
    assert dt == obs_time_t
    assert asdict(sp_result) == pytest.approx(asdict(sun_position))


def test_ints_input_spa(analyzer, obs_time_t, sun_position):
    dt, sp_result = analyzer.sun_position_at(
        year=obs_time_t[0],
        month=obs_time_t[1],
        day=obs_time_t[2],
        hour=obs_time_t[3],
        minute=obs_time_t[4],
        second=obs_time_t[5],
    )
    assert dt == obs_time_t
    assert asdict(sp_result) == pytest.approx(asdict(sun_position))
