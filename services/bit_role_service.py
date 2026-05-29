import json
from datetime import datetime,timedelta

class BitRoleService:
    def __init__(self):
        self.save_path = "data/bit_roles.json"

    def load_data(self):
        try:
            with open(self.save_path, "r", encoding="utf-8)") as file:
                return json.load(file)
        except:
            return {}

    def save_data(self, data):
        with open(self.save_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def create_expiry(self, duration):
        now = datetime.utcnow()

        durations = {
            "hour": timedelta(hours=1),
            "day": timedelta(days=1),
            "month": timedelta(days=30),
            "2months": timedelta(days=60),
            "3months": timedelta(days=90),
            "6months": timedelta(days=180),
            "year": timedelta(days=365),
        }

        if duration == "indefinite":
            return None

        return (now + durations[duration]).timestamp()