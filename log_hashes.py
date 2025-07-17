# log_hashes.py

import hashlib
import time
import json
from typing import List, Dict

class Block:
    def __init__(self, index: int, timestamp: str, data: Dict, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # e.g., {"filename": "...", "hash": "...", "result": "Fake/Real"}
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.ctime(), {"info": "Genesis Block"}, "0")
        self.chain.append(genesis_block)

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_new_block(self, data: Dict):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.ctime(),
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}\n")

# Example usage
if __name__ == "__main__":
    ledger = Blockchain()
    
    # Simulate a fake content verification log
    ledger.add_new_block({
        "filename": "sample_video.mp4",
        "hash": hashlib.sha256(b"sample_video.mp4").hexdigest(),
        "result": "Fake"
    })

    ledger.add_new_block({
        "filename": "news_article.txt",
        "hash": hashlib.sha256(b"Breaking News").hexdigest(),
        "result": "Real"
    })

    ledger.print_chain()

    print("Is blockchain valid?", ledger.is_chain_valid())
