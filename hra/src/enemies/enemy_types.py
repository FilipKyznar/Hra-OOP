from __future__ import annotations

import math
import pygame

from src.config import WIDTH
from src.enemies.base_enemy import Enemy


def _shade(color: tuple[int, int, int], delta: int) -> tuple[int, int, int]:
    return tuple(max(0, min(255, c + delta)) for c in color)


class WalkerEnemy(Enemy):
    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        super().__init__(x, y, 35, 35, color)
        self.speed = 2
        self._build_sprite(color)

    def _build_sprite(self, color: tuple[int, int, int]) -> None:
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, color, pygame.Rect(3, 8, 29, 22), border_radius=8)
        pygame.draw.rect(self.image, _shade(color, -50), pygame.Rect(6, 25, 9, 7), border_radius=3)
        pygame.draw.rect(self.image, _shade(color, -50), pygame.Rect(20, 25, 9, 7), border_radius=3)
        pygame.draw.circle(self.image, (250, 250, 250), (12, 18), 3)
        pygame.draw.circle(self.image, (250, 250, 250), (23, 18), 3)

    def update(self, player=None, speed_scale: float = 1.0) -> None:
        self.rect.x += int(self.speed * speed_scale)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed *= -1


class JumperEnemy(Enemy):
    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        super().__init__(x, y, 30, 30, color)
        self.phase = 0
        self._build_sprite(color)

    def _build_sprite(self, color: tuple[int, int, int]) -> None:
        self.image.fill((0, 0, 0, 0))
        points = [(15, 2), (28, 26), (2, 26)]
        pygame.draw.polygon(self.image, color, points)
        pygame.draw.polygon(self.image, _shade(color, -55), points, 2)
        pygame.draw.circle(self.image, (255, 245, 245), (15, 16), 4)

    def update(self, player=None, speed_scale: float = 1.0) -> None:
        self.phase += 0.2 * speed_scale
        self.rect.y += int(math.sin(self.phase) * (4 * speed_scale))


class ZigZagEnemy(Enemy):
    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        super().__init__(x, y, 32, 32, color)
        self.speed_x = 3
        self.speed_y = 1
        self._build_sprite(color)

    def _build_sprite(self, color: tuple[int, int, int]) -> None:
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, _shade(color, -35), pygame.Rect(0, 0, 32, 32), border_radius=6)
        zig_points = [(4, 10), (12, 5), (20, 12), (28, 6), (28, 14), (20, 22), (12, 16), (4, 23)]
        pygame.draw.polygon(self.image, color, zig_points)
        pygame.draw.circle(self.image, (250, 250, 255), (10, 26), 2)
        pygame.draw.circle(self.image, (250, 250, 255), (22, 26), 2)

    def update(self, player=None, speed_scale: float = 1.0) -> None:
        self.rect.x += int(self.speed_x * speed_scale)
        self.rect.y += int(self.speed_y * speed_scale)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1


class ChaserEnemy(Enemy):
    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        super().__init__(x, y, 30, 40, color)
        self.speed = 2
        self._build_sprite(color)

    def _build_sprite(self, color: tuple[int, int, int]) -> None:
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, color, pygame.Rect(2, 4, 26, 32))
        pygame.draw.ellipse(self.image, _shade(color, 40), pygame.Rect(8, 9, 14, 10))
        pygame.draw.circle(self.image, (255, 255, 255), (11, 20), 3)
        pygame.draw.circle(self.image, (255, 255, 255), (19, 20), 3)
        pygame.draw.rect(self.image, _shade(color, -60), pygame.Rect(9, 30, 12, 6), border_radius=3)

    def update(self, player=None, speed_scale: float = 1.0) -> None:
        if player is None:
            return
        chase_speed = max(1, int(self.speed * speed_scale))
        if player.rect.centerx > self.rect.centerx:
            self.rect.x += chase_speed
        else:
            self.rect.x -= chase_speed


class SpinnerEnemy(Enemy):
    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        super().__init__(x, y, 38, 38, color)
        self.angle = 0
        self.origin_x = x
        self.origin_y = y
        self._build_sprite(color)

    def _build_sprite(self, color: tuple[int, int, int]) -> None:
        self.image.fill((0, 0, 0, 0))
        center = (19, 19)
        pygame.draw.circle(self.image, _shade(color, -40), center, 18)
        pygame.draw.circle(self.image, color, center, 13)
        pygame.draw.circle(self.image, _shade(color, 65), center, 5)
        for spoke in [(19, 2), (35, 19), (19, 35), (2, 19)]:
            pygame.draw.line(self.image, _shade(color, 70), center, spoke, 2)

    def update(self, player=None, speed_scale: float = 1.0) -> None:
        self.angle += 0.12 * speed_scale
        self.rect.x = int(self.origin_x + math.cos(self.angle) * 40)
        self.rect.y = int(self.origin_y + math.sin(self.angle) * 40)
