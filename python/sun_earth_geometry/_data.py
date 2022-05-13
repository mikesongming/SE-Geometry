from dataclasses import dataclass, fields, is_dataclass
from typing import Dict, Optional, Tuple, Type, TypeAlias, TypeVar


@dataclass
class Observatory:
    longitude: float
    latitude: float
    elevation: float
    timezone: float
    delta_ut1: float = 0
    delta_t: float = 0
    pressure: float = 0
    temperature: float = 0
    atmos_refract: float = 0


@dataclass
class TopoCentricSunPositionResult:
    zenith: float
    azimuth: float
    julian_day: Optional[float] = None


@dataclass
class TopoCentricSunRiseTransitSetResult:
    suntransit: float
    sunrise: float
    sunset: float


# @dataclass
# class SunPathResult:
#     pass

OBS_TIME_T: TypeAlias = Tuple[int, int, int, int, int, int]

_Data = TypeVar(
    "_Data",
    Observatory,
    TopoCentricSunPositionResult,
    TopoCentricSunRiseTransitSetResult,
)


def safely_from_dict(d: Dict, cls: Type[_Data]) -> _Data:
    if is_dataclass(cls):
        field_names = {f.name for f in fields(cls)}
        filtered_d = {k: v for k, v in d.items() if k in field_names}
        return cls(**filtered_d)
    else:
        raise TypeError(f"Invalid class type: {cls}")
