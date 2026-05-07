from __future__ import annotations

import pygame

from src.config import GRAVITY, HEIGHT, JUMP_FORCE, PLAYER_SPEED, WIDTH
from src.entities.base_entity import BaseEntity


def _shade(color: tuple[int, int, int], delta: int) -> tuple[int, int, int]:
    return tuple(max(0, min(255, c + delta)) for c in color)


class Player(BaseEntity):
    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        super().__init__(x, y, 40, 50, color)
        self.velocity_y = 0.0
        self.lives = 3
        self._build_sprite(color)

    def _build_sprite(self, color: tuple[int, int, int]) -> None:
        self.image.fill((0, 0, 0, 0))
        dark = _shade(color, -50)
        light = _shade(color, 45)

        pygame.draw.rect(self.image, color, pygame.Rect(6, 10, 28, 32), border_radius=8)
        pygame.draw.rect(self.image, light, pygame.Rect(10, 14, 20, 10), border_radius=4)
        pygame.draw.rect(self.image, dark, pygame.Rect(4, 38, 32, 8), border_radius=4)
        pygame.draw.circle(self.image, (245, 245, 255), (16, 22), 3)
        pygame.draw.circle(self.image, (245, 245, 255), (24, 22), 3)
        pygame.draw.rect(self.image, (30, 35, 65), pygame.Rect(14, 28, 12, 4), border_radius=2)

    def jump(self, boost: bool = False) -> None:
        self.velocity_y = JUMP_FORCE * (1.35 if boost else 1.0)

    def hit_enemy(self) -> None:
        self.lives -= 1

    def update(self, platforms: pygame.sprite.Group):
        keys = pygame.key.get_pressed()
        move_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x += PLAYER_SPEED

        self.rect.x += move_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.velocity_y += GRAVITY
        self.rect.y += int(self.velocity_y)

        landed_platform = None
        if self.velocity_y > 0:
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.jump(platform.is_boost)
                    landed_platform = platform
                    break

        if self.rect.top > HEIGHT:
            self.lives = 0

        return landed_platform
