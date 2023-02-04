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


class Block:
    def __init__(self, prev_hash, miner_id, id=""):
        self.id = uuid4()  #
        if id != "":
            self.id = id
        self.type = BlockType.normal
        self.timestamp = datetime.now().timestamp()
        self.size = 1  #
        self.txn_fees = 0
        self.txns = []  #
        self.prev_hash = prev_hash  #
        self.miner_id = miner_id
        self.children = list()
        self.hash = ""

    def get_copy(self):
        block = Block(self.prev_hash, self.miner_id, self.id)
        block.timestamp = self.timestamp
        block.size = self.size
        block.txns = deepcopy(self.txns)
        block.children = deepcopy(self.children)
        block.hash = self.get_hash()
        return block

    def get_hash(self):
        if self.hash != "":
            return self.hash
        txns_string = ""
        for txn in self.txns:
            txns_string += txn.__str__()
        return sha256(
            str(self.id).encode() + self.prev_hash.encode() + txns_string.encode()
        ).hexdigest()

    def add_txn(self, txn):
        self.txn_fees += txn.txn_fees
        if len(self.txns) < (self.size - 1):
            self.txns.append(txn)
        else:
            raise BlockFullException("Block is full")

    def prepare_block(self):
        coinbase_txn = CoinbaseTransaction(self.miner_id, self.txn_fees)
        self.txns[:0] = coinbase_txn


class GenesisBlock:
    def __init__(self):
        self.id = UUID(int=0)
        self.type = BlockType.genesis
        self.timestamp = datetime.now().timestamp()
        self.children = list()

    def get_hash(self):
        return sha256(str(self.id).encode()).hexdigest()
