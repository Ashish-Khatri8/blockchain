# A general blockchain implementation in python.

# Import required modules.
from datetime import datetime
from flask import Flask, jsonify
import json
import hashlib


# Part 1 - Creating the blockchain.
class Blockchain:
    """A class to implement the blockchain structure."""
    def __init__(self):
        """Initialize the blockchain and the genesis block."""
        self.chain = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        """Creates a new block and adds it to the blockchain."""
        new_block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.chain.append(new_block)
        return new_block

    def get_previous_block(self):
        """Returns the last block added to the blockchain."""
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """Returns the valid proof for the current block."""
        new_proof = 1
        is_valid_proof = False
        while is_valid_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                is_valid_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        """Returns the SHA256 hash of the block."""
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        """Returns True if entire blockchain is valid, otherwise False."""
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True


# Part 2 - Mining the blockchain.

# Creating a web app.
app = Flask(__name__)
# Creating a blockchain.
blockchain = Blockchain()


# Mining a new block.
@app.route("/mine_block", methods=["GET"])
def mine_block():
    """
    Mines a new block in the blockchain.
    And returns the response to the miner.
    """
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # Mining a new block.
    block = blockchain.create_block(proof, previous_hash)

    # Response for the miner.
    response = {
        "message": "Congratulations! You just mined a block!",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200


# Getting the entire blockchain.
@app.route("/get_chain", methods=["GET"])
def get_chain():
    """Returns the entire chain and its length."""
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200


# Checking the validity of the blockchain.
@app.route("/is_valid", methods=["GET"])
def is_valid():
    """Checks if the blockchain is valid or not."""
    if blockchain.is_chain_valid(blockchain.chain):
        response = {
            "message": "All good. The entire blockchain is valid."
        }
    else:
        response = {
            "message": "Blaze-K8. The blockchain is not valid!"
        }
    return jsonify(response)


# Running the app.
app.run(host="0.0.0.0", port=5000)
