from __future__ import annotations

import json
from pathlib import Path


class SaveManager:
    def __init__(self, save_path: str = "save_data.json") -> None:
        self.save_path = Path(save_path)

    def _defaults(self) -> dict:
        return {
            "wallet_coins": 0,
            "best_score": 0,
            "owned_skins": ["Classic"],
            "selected_skin": "Classic",
            "hard_mode": False,
        }

    def load(self) -> dict:
        defaults = self._defaults()
        if not self.save_path.exists():
            return defaults
        try:
            data = json.loads(self.save_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return defaults

        owned = data.get("owned_skins", defaults["owned_skins"])
        if not isinstance(owned, list):
            owned = defaults["owned_skins"]
        if "Classic" not in owned:
            owned.append("Classic")
        selected_skin = str(data.get("selected_skin", "Classic"))
        if selected_skin not in owned:
            selected_skin = "Classic"
        return {
            "wallet_coins": int(data.get("wallet_coins", 0)),
            "best_score": int(data.get("best_score", 0)),
            "owned_skins": owned,
            "selected_skin": selected_skin,
            "hard_mode": bool(data.get("hard_mode", False)),
        }

    def save(
        self,
        wallet_coins: int,
        best_score: int,
        owned_skins: list[str],
        selected_skin: str = "Classic",
        hard_mode: bool = False,
    ) -> None:
        normalized_owned = sorted(list(set(owned_skins)))
        if "Classic" not in normalized_owned:
            normalized_owned.append("Classic")
        normalized_owned.sort()
        if selected_skin not in normalized_owned:
            selected_skin = "Classic"
        payload = {
            "wallet_coins": max(0, int(wallet_coins)),
            "best_score": max(0, int(best_score)),
            "owned_skins": normalized_owned,
            "selected_skin": selected_skin,
            "hard_mode": bool(hard_mode),
        }
        self.save_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
