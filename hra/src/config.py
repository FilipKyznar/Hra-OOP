WIDTH = 900
HEIGHT = 700
FPS = 60

GRAVITY = 0.4
JUMP_FORCE = -14.4
PLAYER_SPEED = 8

PLATFORM_WIDTH = 130
PLATFORM_HEIGHT = 20
INITIAL_PLATFORM_COUNT = 12

ENEMY_SPAWN_CHANCE = 0.08
COIN_SPAWN_CHANCE = 0.35

FONT_NAME = "arial"

SKINS = {
    "Classic": {
        "bg": (20, 20, 40),
        "player": (80, 220, 130),
        "platform": (120, 120, 200),
        "coin": (255, 215, 0),
        "enemy": (220, 90, 90),
    },
    "Neon": {
        "bg": (10, 10, 15),
        "player": (0, 255, 255),
        "platform": (255, 0, 170),
        "coin": (255, 240, 0),
        "enemy": (255, 70, 70),
    },
    "Sunset": {
        "bg": (42, 24, 48),
        "player": (255, 170, 95),
        "platform": (255, 110, 140),
        "coin": (255, 225, 120),
        "enemy": (220, 70, 120),
    },
    "Forest": {
        "bg": (14, 38, 28),
        "player": (132, 245, 132),
        "platform": (72, 175, 102),
        "coin": (244, 220, 108),
        "enemy": (210, 92, 78),
    },
    "Ice": {
        "bg": (16, 30, 58),
        "player": (150, 228, 255),
        "platform": (108, 180, 245),
        "coin": (255, 246, 170),
        "enemy": (255, 120, 145),
    },
}

SKIN_PRICES = {
    "Classic": 0,
    "Neon": 30,
    "Sunset": 45,
    "Forest": 55,
    "Ice": 70,
}
