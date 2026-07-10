import json
import os

CODES_FILE = "data/codes.json"
USERS_FILE = "data/users.json"


class CodesManager:

    def load_codes(self):
        if not os.path.exists(CODES_FILE):
            return []

        with open(CODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_codes(self, codes):
        with open(CODES_FILE, "w", encoding="utf-8") as f:
            json.dump(codes, f, ensure_ascii=False, indent=4)

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            return []

        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_users(self, users):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    def verify_code(self, code):

        codes = self.load_codes()

        for item in codes:

            if item["code"] == code:

                if item["used"]:

                    return {
                        "success": False,
                        "message": "الكود مستخدم مسبقًا."
                    }

                return {
                    "success": True,
                    "data": item
                }

        return {
            "success": False,
            "message": "الكود غير صحيح."
        }

    def activate_code(self, telegram_id, username, code):

        result = self.verify_code(code)

        if not result["success"]:
            return result

        codes = self.load_codes()
        users = self.load_users()

        for item in codes:
            if item["code"] == code:
                item["used"] = True

        users.append({
            "telegram_id": telegram_id,
            "username": username,
            "code": code,
            "subscription": "FREE",
            "consultation_start": None,
            "consultation_end": None,
            "consultations_count": 0
        })

        self.save_codes(codes)
        self.save_users(users)

        return {
            "success": True
        }
