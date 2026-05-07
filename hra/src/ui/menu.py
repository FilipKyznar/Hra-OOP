from __future__ import annotations

import random

import pygame

from src.config import FONT_NAME, HEIGHT, WIDTH


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, label: str, action: str) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.action = action

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, mouse_pos: tuple[int, int]) -> None:
        hovered = self.rect.collidepoint(mouse_pos)
        shadow_rect = self.rect.move(0, 4)
        pygame.draw.rect(screen, (18, 22, 45), shadow_rect, border_radius=14)
        fill_color = (96, 140, 255) if hovered else (58, 86, 188)
        pygame.draw.rect(screen, fill_color, self.rect, border_radius=14)
        pygame.draw.rect(screen, (225, 235, 255), self.rect, 2, border_radius=14)
        text = font.render(self.label, True, (245, 248, 255))
        screen.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - text.get_height() // 2))

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)


class Menu:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont(FONT_NAME, 44)
        self.medium_font = pygame.font.SysFont(FONT_NAME, 28)
        self.small_font = pygame.font.SysFont(FONT_NAME, 22)
        self.main_buttons: list[Button] = []
        self._background = self._build_gradient_background()
        self._particles = self._build_menu_particles()

    def _build_gradient_background(self) -> pygame.Surface:
        bg = pygame.Surface((WIDTH, HEIGHT))
        top = (12, 15, 34)
        bottom = (26, 38, 84)
        for y in range(HEIGHT):
            t = y / HEIGHT
            color = (
                int(top[0] + (bottom[0] - top[0]) * t),
                int(top[1] + (bottom[1] - top[1]) * t),
                int(top[2] + (bottom[2] - top[2]) * t),
            )
            pygame.draw.line(bg, color, (0, y), (WIDTH, y))
        return bg

    def _build_menu_particles(self) -> list[dict]:
        particles = []
        for _ in range(28):
            particles.append(
                {
                    "x": random.randint(0, WIDTH),
                    "y": random.randint(0, HEIGHT),
                    "r": random.randint(2, 4),
                    "speed": random.uniform(0.15, 0.55),
                }
            )
        return particles

    def build_main_buttons(self, preview_skin: str, hard_mode: bool, buy_label: str) -> None:
        x = WIDTH // 2 - 140
        y = 240
        step = 62
        self.main_buttons = [
            Button(x, y, 280, 48, "Start hry", "start"),
            Button(x, y + step, 280, 48, f"Nahled skinu: {preview_skin}", "preview_skin"),
            Button(x, y + step * 2, 280, 48, buy_label, "buy_skin"),
            Button(x, y + step * 3, 280, 48, f"Hard mode: {'ON' if hard_mode else 'OFF'}", "hard"),
            Button(x, y + step * 4, 280, 48, "Konec", "quit"),
        ]

    def draw_main(
        self,
        screen: pygame.Surface,
        preview_skin: str,
        hard_mode: bool,
        wallet_coins: int,
        best_score: int,
        skin_status: str,
        buy_label: str,
    ) -> None:
        self.build_main_buttons(preview_skin, hard_mode, buy_label)
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(self._background, (0, 0))
        tick = pygame.time.get_ticks()

        for particle in self._particles:
            particle["y"] += particle["speed"]
            if particle["y"] > HEIGHT + 6:
                particle["y"] = -8
                particle["x"] = random.randint(0, WIDTH)
            alpha = 90 + int((tick / 8 + particle["x"]) % 120)
            pygame.draw.circle(screen, (190, 215, 255, alpha), (int(particle["x"]), int(particle["y"])), particle["r"])

        header = pygame.Rect(WIDTH // 2 - 315, 34, 630, 172)
        pygame.draw.rect(screen, (15, 20, 44, 150), header, border_radius=24)
        pygame.draw.rect(screen, (120, 140, 255), header, 3, border_radius=24)

        pulse = 225 + int((tick / 12) % 30)
        title = self.font.render("Platform Jumper", True, (pulse, 245, 255))
        subtitle = self.small_font.render("Klikni mysí na tlačítka", True, (195, 205, 255))
        stats = self.small_font.render(f"Penezenka: {wallet_coins}   |   Nejvyssi skore: {best_score}", True, (255, 220, 140))
        skin_info = self.small_font.render(skin_status, True, (185, 255, 205))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 65))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 117))
        screen.blit(stats, (WIDTH // 2 - stats.get_width() // 2, 145))
        screen.blit(skin_info, (WIDTH // 2 - skin_info.get_width() // 2, 172))

        for button in self.main_buttons:
            button.draw(screen, self.medium_font, mouse_pos)

    def draw_pause(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        screen.blit(overlay, (0, 0))
        text = self.font.render("PAUSE - P pokracovat", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    def draw_game_over(self, screen: pygame.Surface, score: int, best_score: int) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        title = self.font.render("Game Over", True, (255, 120, 120))
        score_text = self.small_font.render(f"Skore: {score}", True, (255, 255, 255))
        best_text = self.small_font.render(f"Nejvyssi skore: {best_score}", True, (255, 220, 140))
        restart = self.small_font.render("R - Restart, ESC - Menu", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 2 + 30))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 65))
