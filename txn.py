from uuid import uuid4
from datetime import datetime
from constants import *
from enum import Enum
from node import *

class TxnType(Enum):
    normal = "normal"
    coinbase = "coinbase"

class Transaction:
    def __init__(self, qty, sender, receiver):
        self.id = uuid4()
        self.type = TxnType.normal
        self.qty = qty
        self.sender_id = sender.id
        self.receiver_id = receiver.id
        self.size = TXN_SIZE
        self.timestamp = datetime.now().timestamp()
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


class CoinbaseTransaction:
    def __init__(self, miner_id, txn_fees):
        self.id = uuid4()
        self.type = TxnType.coinbase
        self.fee = MINING_FEE + txn_fees
        self.miner_id = miner_id