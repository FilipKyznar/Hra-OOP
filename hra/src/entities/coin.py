from __future__ import annotations

from src.entities.base_entity import BaseEntity


class Coin(BaseEntity):
    VALUE = 50

    def update(self, *args, **kwargs) -> None:
        return
