from typing import Protocol, Tuple


class ALGORITHM(Protocol):
    def get_observatory(self) -> dict:
        pass

    def set_observatory(self, kwargs):
        pass

    def has_set_observatory(self) -> bool:
        pass

    def calc_sun_position_at(self, year, month, day, hour, minute, second) -> Tuple:
        pass
