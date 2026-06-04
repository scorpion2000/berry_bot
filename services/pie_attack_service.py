import json
import os
import random
import discord


class PieAttackService:

    SCOPE_GENERAL = "General Chat"
    SCOPE_EVERYWHERE = "Everywhere"

    def __init__(self):
        self.active_attacks: dict[int, dict] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists("data/pie_attacks.json"):
            return
 
        with open("data/pie_attacks.json", "r") as f:
            raw: dict[str, dict] = json.load(f)
 
        for str_id, entry in raw.items():
            self.active_attacks[int(str_id)] = {
                "count":        entry["count"],
                "target":       entry["target"],
                "scope":        entry["scope"]
            }
 
    def _save(self) -> None:
        os.makedirs(os.path.dirname("data/pie_attacks.json"), exist_ok=True)
 
        serialisable = {
            str(uid): {
                "count":  entry["count"],
                "target": entry["target"],
                "scope":  entry["scope"]
            }
            for uid, entry in self.active_attacks.items()
        }
 
        with open("data/pie_attacks.json", "w") as f:
            json.dump(serialisable, f, indent=2)


    def start_attack(self, victim: discord.User, scope: str) -> int:
        target = random.randint(15, 50)
        self.active_attacks[victim.id] = {
            "count": 0,
            "target": target,
            "scope": scope
        }
        self._save()
        return target

    def is_under_attack(self, user_id: int) -> bool:
        return user_id in self.active_attacks

    def cancel_attack(self, user_id: int) -> None:
        self.active_attacks.pop(user_id, None)
        self._save()

    def should_track(self, message: discord.Message, general_chat_id: int) -> bool:
        user_id = message.author.id
        if user_id not in self.active_attacks:
            return False

        scope = self.active_attacks[user_id]["scope"]
        if scope == self.SCOPE_GENERAL:
            return message.channel.id == general_chat_id
        return True

    def record_message(self, message: discord.Message) -> bool:
        user_id = message.author.id
        attack = self.active_attacks[user_id]
        attack["count"] += 1
        self._save()
        return attack["count"] >= attack["target"]

    def pop_attack(self, user_id: int) -> dict:
        self._save()
        return self.active_attacks.pop(user_id)
