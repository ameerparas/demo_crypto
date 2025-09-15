import json, time
from .utils import sha256_hex

class Block:
    def __init__(self, index, previous_hash, timestamp=None, transactions=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.transactions = transactions or []
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        tx_str = json.dumps([t.to_dict() for t in self.transactions], sort_keys=True)
        block_str = f"{self.index}{self.previous_hash}{self.timestamp}{tx_str}{self.nonce}"
        return sha256_hex(block_str)

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "nonce": self.nonce,
            "hash": self.hash,
        }
