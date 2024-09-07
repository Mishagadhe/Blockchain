import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, data, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # The genesis block is the first block in the chain
        return Block(0, "0", "Genesis Block", time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

           
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the current block's previous hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                return False

        return True
    # Testing the blockchain
my_blockchain = Blockchain()


my_blockchain.add_block(Block(1, "", "Transaction Data 1", time.time()))
my_blockchain.add_block(Block(2, "", "Transaction Data 2", time.time()))
my_blockchain.add_block(Block(3, "", "Transaction Data 3", time.time()))


for block in my_blockchain.chain:
    print(f"Block {block.index}:")
    print(f"    Previous Hash: {block.previous_hash}")
    print(f"    Data: {block.data}")
    print(f"    Hash: {block.hash}\n")


print("Is the blockchain valid?", my_blockchain.is_chain_valid())

