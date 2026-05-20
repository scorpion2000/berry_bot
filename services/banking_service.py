import json

class BankingService:
    def __init__(self):
        self.bank = self.load_bank()

    def load_bank(self):
        try:
            with open("bit_bank.json", "r") as fp:
                return json.load(fp)
        except FileNotFoundError:
            return {}
    
    def save_bank(self):
        with open("bit_bank.json", "w") as fp:
            json.dump(self.bank, fp)

    
    def get_balance(self, username):
        return self.bank.get(username, 0)

    def add_bits(self, username, amount):
        if self.bank.get(username, 0) + amount < 0:
            return False
        self.bank.update({username : self.bank.get(username, 0) + amount})
        self.save_bank()
        return True

    def transfer_bits(self, sender, receiver, amount):
        if amount <= 0:
            return False, "Amount must be positive."

        sender_balance = self.get_balance(sender)

        if sender_balance < amount:
            return False, (
                f"You only have {sender_balance} bits!"
            )

        self.add_bits(sender, -amount)
        self.add_bits(receiver, amount)

        return True, None