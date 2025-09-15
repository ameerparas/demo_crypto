from blockchain.blockchain import Blockchain
from blockchain.wallet import Wallet

def test_mining_and_balances(tmp_path):
    # use temporary file for persistence
    file = tmp_path / "chain.json"
    bc = Blockchain(difficulty=2, mining_reward=25.0, persist_file=str(file))

    miner = Wallet()
    bc.mine_pending(miner.address)

    assert bc.get_balance(miner.address) == 25.0
    assert bc.is_chain_valid()

def test_double_spend(tmp_path):
    file = tmp_path / "chain.json"
    bc = Blockchain(difficulty=1, mining_reward=50.0, persist_file=str(file))

    miner = Wallet()
    bc.mine_pending(miner.address)

    alice = Wallet()
    # miner -> alice
    msg = miner.address + alice.address + str(20) + "1"
    sig = miner.sign(msg)
    from blockchain.transaction import Transaction
    tx1 = Transaction(miner.address, alice.address, 20, miner.public_key, sig, 1)
    assert bc.add_transaction(tx1)

    # invalid tx: alice tries to spend without balance
    bob = Wallet()
    msg2 = alice.address + bob.address + str(50) + "2"
    sig2 = alice.sign(msg2)
    tx2 = Transaction(alice.address, bob.address, 50, alice.public_key, sig2, 2)
    assert bc.add_transaction(tx2) is False
