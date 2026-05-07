from __future__ import annotations

import random

import pygame

from src.config import (
    COIN_SPAWN_CHANCE,
    ENEMY_SPAWN_CHANCE,
    FPS,
    HEIGHT,
    INITIAL_PLATFORM_COUNT,
    PLATFORM_HEIGHT,
    PLATFORM_WIDTH,
    SKIN_PRICES,
    SKINS,
    WIDTH,
)
from src.core.save_manager import SaveManager
from src.core.state import RuntimeState, Settings
from src.enemies.enemy_types import ChaserEnemy, JumperEnemy, SpinnerEnemy, WalkerEnemy, ZigZagEnemy
from src.entities.coin import Coin
from src.entities.platform import Platform
from src.entities.player import Player
from src.ui.menu import Menu


class Game:
    ENEMY_STOMP_SCORE = 75
    COMBO_TIMEOUT_MS = 2200
    DAMAGE_COOLDOWN_MS = 1200

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Platform Jumper")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.settings = Settings()
        self.state = RuntimeState()
        self.save_manager = SaveManager()
        profile = self.save_manager.load()
        self.wallet_coins = profile["wallet_coins"]
        self.best_score = profile["best_score"]
        self.owned_skins = profile["owned_skins"]
        self.settings.skin_name = profile.get("selected_skin", self.settings.skin_name)
        self.settings.hard_mode = profile.get("hard_mode", self.settings.hard_mode)
        self.skin_catalog = list(SKINS.keys())
        if self.settings.skin_name not in self.owned_skins:
            self.settings.skin_name = self.owned_skins[0]
        self.preview_skin_index = self.skin_catalog.index(self.settings.skin_name)
        self.mode = "menu"
        self.camera_y = 0.0
        self.font = pygame.font.SysFont("arial", 24)
        self.title_font = pygame.font.SysFont("arial", 28, bold=True)
        self.menu_message = "Vyber skin nebo klikni Start."
        self.enemy_types = [WalkerEnemy, JumperEnemy, ZigZagEnemy, ChaserEnemy, SpinnerEnemy]
        self.world_background = self._build_world_background()
        self.star_layers = self._build_star_layers()
        self.stomp_combo = 0
        self.combo_timer = 0
        self.damage_cooldown = 0
        self._create_world()

    def _build_world_background(self) -> pygame.Surface:
        bg = pygame.Surface((WIDTH, HEIGHT))
        top = (8, 10, 25)
        bottom = (20, 34, 70)
        for y in range(HEIGHT):
            t = y / HEIGHT
            color = (
                int(top[0] + (bottom[0] - top[0]) * t),
                int(top[1] + (bottom[1] - top[1]) * t),
                int(top[2] + (bottom[2] - top[2]) * t),
            )
            pygame.draw.line(bg, color, (0, y), (WIDTH, y))
        return bg

    def _build_star_layers(self) -> list[list[tuple[int, int, int]]]:
        layers: list[list[tuple[int, int, int]]] = []
        densities = [22, 16, 10]
        for density in densities:
            stars = []
            for _ in range(density):
                stars.append((random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)))
            layers.append(stars)
        return layers

    def _current_skin(self) -> dict[str, tuple[int, int, int]]:
        return SKINS[self.settings.skin_name]

    def _platform_color(self, platform_type: str) -> tuple[int, int, int]:
        base = self._current_skin()["platform"]
        if platform_type == "breakable":
            return (250, 165, 90)
        if platform_type == "boost":
            return (120, 255, 170)
        return base

    def _pick_platform_type(self) -> str:
        roll = random.random()
        if roll < 0.12:
            return "breakable"
        if roll < 0.17:
            return "boost"
        return "normal"

    def _create_world(self) -> None:
        colors = self._current_skin()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        base_y = HEIGHT - 40
        for i in range(INITIAL_PLATFORM_COUNT):
            y = base_y - i * 75
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            platform_type = "normal" if i < 3 else self._pick_platform_type()
            self.platforms.add(
                Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, self._platform_color(platform_type), platform_type)
            )

        self.player = Player(WIDTH // 2, HEIGHT - 130, colors["player"])
        self.player.jump()
        self.camera_y = 0
        self.stomp_combo = 0
        self.combo_timer = 0
        self.damage_cooldown = 0
        self.state = RuntimeState()

    def _save_profile(self) -> None:
        self.save_manager.save(
            self.wallet_coins,
            self.best_score,
            self.owned_skins,
            self.settings.skin_name,
            self.settings.hard_mode,
        )

    def _update_best_score(self) -> None:
        if self.state.score > self.best_score:
            self.best_score = self.state.score
            self._save_profile()

    def _spawn_new_rows(self) -> None:
        highest_platform_y = min(platform.rect.y for platform in self.platforms)
        difficulty = min(40, int(self.state.score // 300))
        min_gap = max(48, 60 - difficulty)
        max_gap = max(80, 98 - difficulty)
        while highest_platform_y > self.camera_y - HEIGHT:
            highest_platform_y -= random.randint(min_gap, max_gap)
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            colors = self._current_skin()
            platform_type = self._pick_platform_type()
            platform = Platform(
                x,
                highest_platform_y,
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT,
                self._platform_color(platform_type),
                platform_type,
            )
            self.platforms.add(platform)

            if random.random() < COIN_SPAWN_CHANCE:
                self.coins.add(Coin(x + PLATFORM_WIDTH // 2 - 10, highest_platform_y - 30, 20, 20, colors["coin"]))

            spawn_bonus = min(0.22, self.state.score / 9000)
            chance = (ENEMY_SPAWN_CHANCE + spawn_bonus) * (2 if self.settings.hard_mode else 1)
            if random.random() < chance:
                extra_enemy_chance = min(0.8, 0.45 + self.state.score / 7000)
                spawn_count = 2 if random.random() < extra_enemy_chance else 1
                for _ in range(spawn_count):
                    enemy_class = random.choice(self.enemy_types)
                    offset_x = random.randint(0, max(1, PLATFORM_WIDTH - 40))
                    self.enemies.add(enemy_class(x + offset_x, highest_platform_y - 35, colors["enemy"]))

    def _despawn_old(self) -> None:
        cutoff = self.camera_y + HEIGHT + 120
        for group in (self.platforms, self.coins, self.enemies):
            for sprite in list(group):
                if sprite.rect.top > cutoff:
                    group.remove(sprite)

    def _update_camera_and_score(self) -> None:
        target_camera = min(self.camera_y, self.player.rect.y - HEIGHT // 3)
        if target_camera < self.camera_y:
            self.camera_y += (target_camera - self.camera_y) * 0.16
        else:
            self.camera_y = target_camera
        self.state.best_height = max(self.state.best_height, -self.camera_y)
        self.state.score = int(self.state.best_height / 10) + self.state.coins * 10 + self.state.bonus_score

    def _handle_collisions(self) -> None:
        coins = pygame.sprite.spritecollide(self.player, self.coins, dokill=True)
        if coins:
            self.state.coins += len(coins)
            self.wallet_coins += len(coins)
            self._save_profile()

        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, dokill=False)
        if enemy_hits:
            stomped_enemy = None
            for enemy in enemy_hits:
                if self.player.velocity_y > 0 and self.player.rect.bottom <= enemy.rect.centery + 6:
                    stomped_enemy = enemy
                    break

            if stomped_enemy is not None:
                self.enemies.remove(stomped_enemy)
                self.player.jump()
                self.stomp_combo += 1
                self.combo_timer = self.COMBO_TIMEOUT_MS
                self.state.bonus_score += self.ENEMY_STOMP_SCORE * self.stomp_combo
            elif self.damage_cooldown == 0:
                self.stomp_combo = 0
                self.combo_timer = 0
                self.player.hit_enemy()
                self.damage_cooldown = self.DAMAGE_COOLDOWN_MS
                self.player.rect.y -= 60
                if self.player.lives <= 0:
                    self.state.game_over = True
                    self._update_best_score()
                    self.mode = "game_over"

    def _update_game(self) -> None:
        dt = self.clock.get_time()
        if self.damage_cooldown > 0:
            self.damage_cooldown = max(0, self.damage_cooldown - dt)
        if self.combo_timer > 0:
            self.combo_timer = max(0, self.combo_timer - dt)
            if self.combo_timer == 0:
                self.stomp_combo = 0

        landed_platform = self.player.update(self.platforms)
        if landed_platform and landed_platform.is_breakable:
            self.platforms.remove(landed_platform)
        self.coins.update()
        speed_scale = min(3.0, 1.0 + self.state.score / 2500)
        for enemy in self.enemies:
            enemy.update(self.player, speed_scale)

        if self.player.lives <= 0:
            self.state.game_over = True
            self._update_best_score()
            self.mode = "game_over"
            return

        self._update_camera_and_score()
        self._spawn_new_rows()
        self._despawn_old()
        self._handle_collisions()
        self._update_camera_and_score()

    def _draw_world(self) -> None:
        self.screen.blit(self.world_background, (0, 0))
        offset = int(-self.camera_y)
        layer_factors = [0.12, 0.2, 0.3]
        for layer_idx, stars in enumerate(self.star_layers):
            parallax_offset = int(offset * layer_factors[layer_idx]) % HEIGHT
            for x, y, radius in stars:
                draw_y = (y + parallax_offset) % HEIGHT
                brightness = 120 + layer_idx * 45
                pygame.draw.circle(self.screen, (brightness, brightness, 255), (x, draw_y), radius)

        for group in (self.platforms, self.coins, self.enemies):
            for sprite in group:
                self.screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y + offset))
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y + offset))

        hud_panel = pygame.Surface((290, 152), pygame.SRCALPHA)
        hud_panel.fill((12, 16, 32, 165))
        self.screen.blit(hud_panel, (10, 10))
        pygame.draw.rect(self.screen, (110, 130, 255), pygame.Rect(10, 10, 290, 152), 2, border_radius=12)

        hud = [
            f"Skore: {self.state.score}",
            f"Coiny: {self.state.coins}",
            f"Zivoty: {self.player.lives}",
            f"Combo: x{max(1, self.stomp_combo)}",
            f"Stit: {'ON' if self.damage_cooldown else 'OFF'}",
            "P - Pauza",
        ]
        label = self.title_font.render("RUN", True, (180, 210, 255))
        self.screen.blit(label, (20, 16))
        for i, item in enumerate(hud):
            text = self.font.render(item, True, (240, 240, 240))
            self.screen.blit(text, (20, 46 + i * 24))

        if self.damage_cooldown > 0:
            shield = self.font.render(f"Ochrana: {self.damage_cooldown / 1000:.1f}s", True, (130, 255, 230))
            self.screen.blit(shield, (20, 166))

    def _toggle_skin(self) -> None:
        names = list(SKINS.keys())
        idx = names.index(self.settings.skin_name)
        self.settings.skin_name = names[(idx + 1) % len(names)]

    def _preview_next_skin(self) -> None:
        self.preview_skin_index = (self.preview_skin_index + 1) % len(self.skin_catalog)
        preview_skin = self.skin_catalog[self.preview_skin_index]
        if preview_skin in self.owned_skins:
            self.menu_message = f"Nahled: {preview_skin} (vlastnis)."
        else:
            self.menu_message = f"Nahled: {preview_skin} (cena {SKIN_PRICES.get(preview_skin, 0)} coinu)."

    def _buy_or_select_preview_skin(self) -> None:
        preview_skin = self.skin_catalog[self.preview_skin_index]
        if preview_skin in self.owned_skins:
            self.settings.skin_name = preview_skin
            self.menu_message = f"Skin zmenen na {preview_skin}."
            self._save_profile()
            return

        price = SKIN_PRICES.get(preview_skin, 0)
        if self.wallet_coins >= price:
            self.wallet_coins -= price
            self.owned_skins.append(preview_skin)
            self.settings.skin_name = preview_skin
            self.menu_message = f"Koupen skin {preview_skin} za {price} coinu."
            self._save_profile()
        else:
            self.menu_message = f"Skin {preview_skin} stoji {price} coinu."

    def _skin_buy_label(self) -> str:
        preview_skin = self.skin_catalog[self.preview_skin_index]
        if preview_skin in self.owned_skins:
            return f"Pouzit skin ({preview_skin})"
        return f"Koupit skin ({SKIN_PRICES.get(preview_skin, 0)})"

    def _handle_menu_action(self, action: str) -> bool:
        if action == "start":
            self._create_world()
            self.mode = "running"
        elif action == "preview_skin":
            self._preview_next_skin()
        elif action == "buy_skin":
            self._buy_or_select_preview_skin()
        elif action == "hard":
            self.settings.hard_mode = not self.settings.hard_mode
            self._save_profile()
        elif action == "quit":
            return False
        return True

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.mode == "menu" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.menu.main_buttons:
                    if button.is_clicked(event.pos):
                        return self._handle_menu_action(button.action)

            if event.type == pygame.KEYDOWN:
                if self.mode == "menu":
                    if event.key == pygame.K_RETURN:
                        return self._handle_menu_action("start")
                    elif event.key == pygame.K_s:
                        return self._handle_menu_action("preview_skin")
                    elif event.key == pygame.K_b:
                        return self._handle_menu_action("buy_skin")
                    elif event.key == pygame.K_h:
                        return self._handle_menu_action("hard")
                    elif event.key == pygame.K_ESCAPE:
                        return False

                elif self.mode == "running":
                    if event.key == pygame.K_p:
                        self.mode = "paused"
                    elif event.key == pygame.K_ESCAPE:
                        self.mode = "menu"

                elif self.mode == "paused":
                    if event.key == pygame.K_p:
                        self.mode = "running"

                elif self.mode == "game_over":
                    if event.key == pygame.K_r:
                        self._create_world()
                        self.mode = "running"
                    elif event.key == pygame.K_ESCAPE:
                        self.mode = "menu"
        return True

    def run(self) -> None:
        running = True
        while running:
            running = self._handle_events()
            if self.mode == "running":
                self._update_game()
                self._draw_world()
            elif self.mode == "paused":
                self._draw_world()
                self.menu.draw_pause(self.screen)
            elif self.mode == "menu":
                self.menu.draw_main(
                    self.screen,
                    self.skin_catalog[self.preview_skin_index],
                    self.settings.hard_mode,
                    self.wallet_coins,
                    self.best_score,
                    self.menu_message,
                    self._skin_buy_label(),
                )
            elif self.mode == "game_over":
                self._draw_world()
                self.menu.draw_game_over(self.screen, self.state.score, self.best_score)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
