from __future__ import annotations

import pygame


class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: int, height: int, color: tuple[int, int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, *args, **kwargs) -> None:
        raise NotImplementedError("Subclasses must implement update().")
