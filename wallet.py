import os, time
from .utils import sha256_hex

try:
    from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError
    USE_ECDSA = True
except:
    USE_ECDSA = False

class Wallet:
    def __init__(self):
        if USE_ECDSA:
            self._sk = SigningKey.generate(curve=SECP256k1)
            self._vk = self._sk.get_verifying_key()
            self.private_key = self._sk.to_string().hex()
            self.public_key = self._vk.to_string().hex()
        else:
            t = str(time.time()) + os.urandom(8).hex()
            self.private_key = sha256_hex('priv'+t)
            self.public_key = sha256_hex('pub'+t)

        self.address = sha256_hex(self.public_key)[:40]

    def sign(self, message: str) -> str:
        if USE_ECDSA:
            sig = self._sk.sign(message.encode('utf-8'))
            return sig.hex()
        return sha256_hex(self.private_key + message)

    @staticmethod
    def verify(public_key_hex: str, message: str, signature_hex: str) -> bool:
        if USE_ECDSA:
            try:
                vk = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
                vk.verify(bytes.fromhex(signature_hex), message.encode('utf-8'))
                return True
            except Exception:
                return False
        return sha256_hex(public_key_hex + message) == signature_hex
