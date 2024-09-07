import hashlib
import time
import ecdsa

class Block:
    def __init__(self, index, previous_hash, data, timestamp, difficulty=4):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        while self.hash[:self.difficulty] != "0" * self.difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined with nonce: {self.nonce} and hash: {self.hash}")

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None

    def sign_transaction(self, private_key):
        private_key_object = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        message = f"{self.sender}{self.receiver}{self.amount}".encode()
        self.signature = private_key_object.sign(message).hex()

    def is_valid(self):
        if not self.signature:
            return False
        public_key_object = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve=ecdsa.SECP256k1)
        try:
            public_key_object.verify(bytes.fromhex(self.signature), f"{self.sender}{self.receiver}{self.amount}".encode())
            return True
        except ecdsa.BadSignatureError:
            return False

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.mining_reward = 50
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block", time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def mine_pending_transactions(self, miner_address):
        block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions, time.time())
        block.mine_block()
        self.chain.append(block)
        self.pending_transactions = [Transaction(None, miner_address, self.mining_reward)]

    def create_transaction(self, sender, receiver, amount, private_key):
        transaction = Transaction(sender, receiver, amount)
        transaction.sign_transaction(private_key)
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
        else:
            print("Invalid transaction")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
