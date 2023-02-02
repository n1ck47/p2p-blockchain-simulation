from datetime import datetime
from uuid import uuid4
from txn import Transaction, CoinbaseTransaction
from exceptions import BlockFullException
from constants import *
from enum import Enum

class BlockType(Enum):
    normal = "normal"
    genesis = "genesis"

class Block:
    def __init__(self, prev_hash):
        self.id = uuid4() #
        self.type = BlockType.normal 
        self.timestamp = datetime.now().timestamp()
        self.size = BLOCK_SIZE #
        self.txn_fees = 0
        self.txns = [] #
        self.prev_hash = prev_hash #
        # self.miner_id = miner_id 
        self.children=list() 
    
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
        self.hash = '0'*256
        self.children=list()


    
