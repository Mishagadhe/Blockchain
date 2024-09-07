from flask import Flask, jsonify, request
import blockchain

app = Flask(__name__)
my_blockchain = blockchain.Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in my_blockchain.chain:
        chain_data.append({
            'index': block.index,
            'previous_hash': block.previous_hash,
            'data': block.data,
            'hash': block.hash
        })
    return jsonify(chain_data), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required_fields = ['sender', 'receiver', 'amount', 'private_key']
    if not all(field in values for field in required_fields):
        return 'Missing fields', 400

    sender = values['sender']
    receiver = values['receiver']
    amount = values['amount']
    private_key = values['private_key']
    
    my_blockchain.create_transaction(sender, receiver, amount, private_key)
    return 'Transaction added', 201

@app.route('/mine', methods=['GET'])
def mine():
    miner_address = request.args.get('miner_address')
    if not miner_address:
        return 'Miner address is required', 400

    my_blockchain.mine_pending_transactions(miner_address)
    return 'Block mined and reward given', 200

@app.route('/validate', methods=['GET'])
def validate_chain():
    if my_blockchain.is_chain_valid():
        return 'Blockchain is valid', 200
    else:
        return 'Blockchain is invalid', 400

if __name__ == '__main__':
    app.run(port=5000)
