# Simple Blockchain in Python

This project demonstrates the basic principles of a blockchain, implemented in Python. Blocks store data and are linked together using cryptographic hashes. Each block contains:
- Index
- Previous block’s hash
- Data (e.g., transaction information)
- Timestamp
- Current block’s hash (calculated using SHA-256)

## Features
- Create a blockchain with an initial "genesis" block.
- Add new blocks with transaction data.
- Verify the integrity of the blockchain.

## How to Run
1. Clone the repository: `git clone <repo-link>`
2. Run the script: `python blockchain.py`
