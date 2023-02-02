from datetime import datetime
from uuid import uuid4
from hashlib import sha256
from txn import Transaction, CoinbaseTransaction
from exceptions import BlockFullException
from constants import *
from enum import Enum

class BlockType(Enum):
    normal = "normal"
    genesis = "genesis"

class Block:
    def __init__(self, prev_hash, miner_id):
        self.id = uuid4() #
        self.type = BlockType.normal 
        self.timestamp = datetime.now().timestamp()
        self.size = 1 #
        self.txn_fees = 0
        self.txns = [] #
        self.prev_hash = prev_hash #
        self.miner_id = miner_id 
        self.children=list() 
    
    def get_hash(self):
        txns_string = ""
        for txn in self.txns:
            txns_string += txn.__str__()
        return sha256(str(self.id).encode() + self.prev_hash.encode() + txns_string.encode()).hexdigest()

    def add_txn(self, txn):
        self.txn_fees += txn.txn_fees
        if len(self.txns) < (self.size-1):
            self.txns.append(txn)
        else:
            raise BlockFullException("Block is full")
    
    def prepare_block(self):
        coinbase_txn = CoinbaseTransaction(self.miner_id,self.txn_fees)
        self.txns[:0] = coinbase_txn
    
class GenesisBlock:
    def __init__(self):
        self.id = uuid4()
        self.type = BlockType.genesis
        self.timestamp = datetime.now().timestamp()
        self.hash = sha256('0'.encode()).hexdigest()
        self.children=list()

    def get_hash(self):
        return self.hash


    
