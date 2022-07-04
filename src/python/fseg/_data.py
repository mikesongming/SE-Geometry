from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, TypeAlias, Union

# make_dataclass generated cls is consider an invalid type by mypy
"""
Observatory = make_dataclass(
    "Observatory",
    fields=[
        (fld, float)
        if fld in ["longitude", "latitude", "elevation", "timezone"]
        else (fld, float, field(default=0.0))  # type: ignore
        for fld in Algorithm.OBS_FIELDS
    ],
)
"""


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


LocalDateTime: TypeAlias = Tuple[int, int, int, int, int, int]
Observatory_INPUT: TypeAlias = Union[Observatory, dict]
DateTime_INPUT: TypeAlias = Union[str, datetime, LocalDateTime]


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


# OBS_TIME_T: TypeAlias = Tuple[int, int, int, int, int, int]
# _Data = TypeVar(
#     "_Data",
#     Type[Observatory],
#     TopoCentricSunPositionResult,
#     TopoCentricSunRiseTransitSetResult,
# )
# def safely_from_dict(d: Dict, cls: Type[_Data]) -> _Data:
#     """
#     generate dataclass from dict by dropping irrelevant keys
#     Args:
#         d (Dict): data dict
#         cls (Type[_Data]): data class type
#     Raises:
#         TypeError: failed to generate data class
#     Returns:
#         _Data: data class of type <cls>
#     Examples:
#         >>> d = {'timezone': -7.0, 'longitude': -105.1786, 'latitude': 39.742476,
#         ... 'elevation': 1830.14, 'foo': 100.0}
#         >>> safely_from_dict(d, Observatory)
#         Observatory(longitude=-105.1786, latitude=39.742476, elevation=1830.14,
#         timezone=-7.0, delta_ut1=0, delta_t=0, pressure=0, temperature=0,
#         atmos_refract=0)
#     """
#     if is_dataclass(cls):
#         field_names = {f.name for f in fields(cls)}
#         filtered_d = {k: v for k, v in d.items() if k in field_names}
#         return cls(**filtered_d)
#     else:
#         raise TypeError(f"Invalid class type: {cls}")
