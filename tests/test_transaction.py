import time
from blockchain.wallet import Wallet
from blockchain.transaction import Transaction
from blockchain.blockchain import Blockchain

def test_transaction_valid(monkeypatch):
    bc = Blockchain(difficulty=1, mining_reward=50.0, persist_file=":memory:")

    miner = Wallet()
    # mine once to give balance
    bc.mine_pending(miner.address)

    recipient = Wallet()
    msg = miner.address + recipient.address + str(10) + str(time.time())
    sig = miner.sign(msg)

    tx = Transaction(miner.address, recipient.address, 10, miner.public_key, sig, time.time())
    assert tx.valid(bc) is True

def test_transaction_invalid_signature():
    bc = Blockchain(difficulty=1, mining_reward=50.0, persist_file=":memory:")
    sender, recipient = Wallet(), Wallet()

    msg = sender.address + recipient.address + str(5) + str(time.time())
    sig = recipient.sign(msg)  # wrong signer

    tx = Transaction(sender.address, recipient.address, 5, sender.public_key, sig)
    assert tx.valid(bc) is False
