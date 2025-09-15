from blockchain.block import Block
from blockchain.transaction import Transaction

def test_block_hash_changes_with_nonce():
    b1 = Block(1, "0", 1234567890, [], 0)
    h1 = b1.hash
    b1.nonce += 1
    h2 = b1.compute_hash()
    assert h1 != h2
