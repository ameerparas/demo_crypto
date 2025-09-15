import time, json
from .utils import sha256_hex
from .wallet import Wallet

class Transaction:
    def __init__(self, sender, recipient, amount, public_key, signature, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.public_key = public_key
        self.signature = signature
        self.timestamp = timestamp or time.time()

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "public_key": self.public_key,
            "signature": self.signature,
            "timestamp": self.timestamp,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    def id(self) -> str:
        return sha256_hex(self.to_json())

    def valid(self, chain) -> bool:
        if self.amount <= 0:
            return False
        if not Wallet.verify(
            self.public_key,
            self.sender + self.recipient + str(self.amount) + str(self.timestamp),
            self.signature
        ):
            return False
        if self.sender != "0" and chain.get_balance(self.sender) < self.amount:
            return False
        return True
