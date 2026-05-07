from dataclasses import dataclass


@dataclass
class Settings:
    skin_name: str = "Classic"
    hard_mode: bool = False


@dataclass
class RuntimeState:
    score: int = 0
    coins: int = 0
    bonus_score: int = 0
    best_height: float = 0
    game_over: bool = False
