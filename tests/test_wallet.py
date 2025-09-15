import pytest
from blockchain.wallet import Wallet

def test_wallet_address_unique():
    w1, w2 = Wallet(), Wallet()
    assert w1.address != w2.address

def test_sign_and_verify():
    wallet = Wallet()
    message = "test message"
    sig = wallet.sign(message)
    assert Wallet.verify(wallet.public_key, message, sig) is True

def test_verify_fail():
    w1, w2 = Wallet(), Wallet()
    message = "hello"
    sig = w1.sign(message)
    assert Wallet.verify(w2.public_key, message, sig) is False
