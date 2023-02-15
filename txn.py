from datetime import datetime
from enum import Enum
from uuid import uuid4

from constants import *
from node import *


class TxnType(Enum):
    normal = "normal"
    coinbase = "coinbase"


class Transaction:              #Class for generating transaction
    def __init__(self, env, qty, sender, receiver):
        self.id = uuid4()
        self.type = TxnType.normal
        self.qty = qty
        self.sender_id = sender.id
        self.receiver_id = receiver.id
        self.size = TXN_SIZE
        self.timestamp = env.now
        self.txn_fees = TXN_FEE

    def __str__(self):
        string = (
            str(self.id)
            + ": "
            + str(self.sender_id)
            + " pays "
            + str(self.receiver_id)
            + " "
            + str(self.qty)
            + " coins."
        )
        return string


class CoinbaseTransaction:          #Class for generating coinbase transaction
    def __init__(self, env, miner_id):
        self.id = uuid4()
        self.type = TxnType.coinbase
        self.fee = MINING_FEE
        self.miner_id = miner_id
        self.timestamp = env.now
