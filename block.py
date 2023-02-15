from copy import deepcopy
from datetime import datetime
from enum import Enum
from hashlib import sha256
from uuid import UUID, uuid4

from constants import *
from exceptions import BlockFullException
from txn import CoinbaseTransaction


class BlockType(Enum):
    normal = "normal"
    genesis = "genesis"


class Block:         #Class to create blocks
    def __init__(self, env, prev_hash, miner_id, id=""):
        self.id = str(uuid4())  #
        if id != "":
            self.id = id
        self.type = BlockType.normal
        self.timestamp = env.now
        self.size = 1  #
        self.txn_fees = 0
        self.txns = []  #
        self.prev_hash = prev_hash  #
        self.miner_id = miner_id
        self.children = list()
        self.hash = ""
        self.txn_hash = ""
        self.env = env
        self.balance = list()

    def get_copy(self):       #Method to get the copy of the block
        block = Block(self.env, self.prev_hash, self.miner_id, self.id)
        block.timestamp = self.timestamp
        block.size = self.size
        block.txns = deepcopy(self.txns)
        block.balance = deepcopy(self.balance)
        block.children = deepcopy(self.children)
        block.hash = self.get_hash()
        return block

    def get_hash(self):         #This method returns the hash of the block
        if self.hash != "":
            return self.hash
        if self.txn_hash == "":
            txns_string = ""
            for txn in self.txns:
                txns_string += txn.__str__()
            self.txn_hash = sha256(txns_string.encode()).hexdigest()
        self.hash =  sha256(
            str(self.id).encode() + self.prev_hash.encode() + self.txn_hash.encode()
        ).hexdigest()                       #hash of block is generated using block id ,parent hash and transaction hash
        return self.hash

    def add_txn(self, txn):         #This method adds transaction in the block
        self.txn_fees += txn.txn_fees
        if len(self.txns) < (self.size - 1):
            self.txns.append(txn)
        else:
            raise BlockFullException("Block is full")

    def prepare_block(self):
        coinbase_txn = CoinbaseTransaction(self.miner_id, self.txn_fees)       #Block will be prepared and coinbase transaction added to each block
        self.txns[:0] = coinbase_txn


class GenesisBlock:             #Class for genesis Block
    def __init__(self, env, n):
        self.id = UUID(int=0)
        self.type = BlockType.genesis
        self.timestamp = env.now
        self.children = list()
        self.balance = [NODE_STARTING_BALANCE]*n

    def get_hash(self):
        return sha256(str(self.id).encode()).hexdigest()
