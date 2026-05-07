from __future__ import annotations

from src.entities.base_entity import BaseEntity


class Enemy(BaseEntity):
    DAMAGE = 1

    def on_player_collision(self) -> int:
        return self.DAMAGE
