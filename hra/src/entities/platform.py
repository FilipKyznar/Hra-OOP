from __future__ import annotations

from src.entities.base_entity import BaseEntity


class Platform(BaseEntity):
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: tuple[int, int, int],
        platform_type: str = "normal",
    ) -> None:
        super().__init__(x, y, width, height, color)
        self.platform_type = platform_type

    @property
    def is_breakable(self) -> bool:
        return self.platform_type == "breakable"

    @property
    def is_boost(self) -> bool:
        return self.platform_type == "boost"

    def update(self, *args, **kwargs) -> None:
        return
