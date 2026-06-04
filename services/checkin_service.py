import json
import os
from datetime import datetime, timezone
from config import MAX_LEVEL

DATA_PATH = "data/checkins.json"
TIMEOUT_HOURS = 48


class CheckInService:

    def __init__(self):
        self.data: dict[int, dict] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(DATA_PATH):
            return

        with open(DATA_PATH, "r") as f:
            raw: dict[str, dict] = json.load(f)

        for str_id, entry in raw.items():
            self.data[int(str_id)] = entry

    def _save(self) -> None:
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        serialisable = {
            str(uid): entry
            for uid, entry in self.data.items()
        }

        with open(DATA_PATH, "w") as f:
            json.dump(serialisable, f, indent=2)

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _has_timed_out(self, last_checkin_iso: str) -> bool:
        last = datetime.fromisoformat(last_checkin_iso)
        delta = datetime.now(timezone.utc) - last
        return delta.total_seconds() > TIMEOUT_HOURS * 3600

    def _checked_in_today(self, last_checkin_iso: str) -> bool:
        last = datetime.fromisoformat(last_checkin_iso)
        now = datetime.now(timezone.utc)
        return last.date() == now.date()

    def _get_entry(self, user_id: int) -> dict:
        return self.data.get(user_id, {"level": 0, "last_checkin": None})

    def sweep_timeouts(self) -> list[int]:
        reset_ids = []

        for user_id, entry in self.data.items():
            if entry["last_checkin"] and self._has_timed_out(entry["last_checkin"]):
                self.data[user_id] = {"level": 0, "last_checkin": None}
                reset_ids.append(user_id)

        if reset_ids:
            self._save()

        return reset_ids

    def check_in(self, user_id: int) -> dict:
        entry = self._get_entry(user_id)

        # Guard against checking in twice on the same UTC day
        if entry["last_checkin"] and self._checked_in_today(entry["last_checkin"]):
            return {
                "status": "already_checked_in",
                "level": entry["level"],
                "capped": entry["level"] >= MAX_LEVEL,
            }

        new_level = min(entry["level"] + 1, MAX_LEVEL)
        capped = new_level == MAX_LEVEL and entry["level"] == MAX_LEVEL

        self.data[user_id] = {
            "level": new_level,
            "last_checkin": self._now_iso(),
        }
        self._save()

        return {
            "status": "leveled_up",
            "level": new_level,
            "capped": capped,
        }

    def get_level(self, user_id: int) -> dict:
        entry = self._get_entry(user_id)
        return {
            "level": entry["level"],
            "last_checkin": entry.get("last_checkin"),
        }
