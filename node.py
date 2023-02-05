import random
from functools import reduce
from math import ceil
import numpy as np

from block import Block
from blockchain import Blockchain
from constants import *
from txn import CoinbaseTransaction, Transaction


class Node:
    network = list()

    def __init__(self, id, env, is_fast, cpu_high, n, txn_time, mining_time):
        self.id = id
        self.env = env
        self.prop_delay = np.random.uniform(PROP_DELAY_MIN, PROP_DELAY_MAX)
        self.is_fast = is_fast  # Is node fast or slow?
        self.cpu_high = (
            cpu_high  # Does the node have a high computing powered cpu or not?
        )
        self.neighbours = list()
        self.hashing_power = 0
        self.txn_pool = list()
        self.n = n
        self.txn_time = txn_time
        self.mining_time = mining_time
        self.balance = [NODE_STARTING_BALANCE for i in range(self.n)]
        self.blockchain = Blockchain()

    def compute_delay(self, msg_size, receiver):  # msg_size in KB
        link_speed = SLOW_LINK_SPEED  # in Mbps
        if self.is_fast and receiver.is_fast:
            link_speed = FAST_LINK_SPEED

        queueing_delay = np.random.exponential((float(96)) / (link_speed * 1024))
        return queueing_delay + self.prop_delay + (msg_size * 8) / (link_speed * 1024)

    def generate_txn(self):
        itr=0
        while True:
            if self.balance[self.id] == 0:
                continue
            n = len(self.network)
            receiver_id = self.id
            while self.id == receiver_id:
                receiver_id = random.randint(0, n - 1)

            # payment = random.randint(1, self.balance[self.id] * 2)
            payment = 50
            if payment > self.balance[self.id]:
                continue

            txn = Transaction(payment, self, self.network[receiver_id])
            self.txn_pool.append(txn)
            delay = np.random.exponential(self.txn_time)
            self.env.process(self.broadcast_mssg(None, txn, "txn"))
            yield self.env.timeout(delay)
            itr+=1
            if(itr>40):
                break

    def mine_block(self):
        while True:
            parent_block = self.blockchain.get_last_block()
            delay = np.random.exponential(self.mining_time / self.hashing_power)
            yield self.env.timeout(delay)

            current_parent_block = self.blockchain.get_last_block()

            if parent_block.get_hash() != current_parent_block.get_hash():
                continue

            mined_block = Block(parent_block.get_hash(), self.id)
            mined_block.txns.append(CoinbaseTransaction(self.id))
            mined_block.size += 1

            itr = 0
            while itr < len(self.txn_pool):
                if itr >= 1022 or len(self.txn_pool) == 0:
                    break

                txn = self.txn_pool.pop(0)
                if self.balance[txn.sender_id] < txn.qty:
                    continue

                self.balance[txn.sender_id] -= txn.qty
                self.balance[txn.receiver_id] += txn.qty
                mined_block.txns.append(txn)
                mined_block.size += 1
                itr += 1

            self.balance[self.id] += 50
            self.blockchain.add_block(mined_block)
            self.env.process(self.mine_block())

            yield self.env.process(self.broadcast_mssg(None, mined_block, "block"))
            break

    def broadcast_mssg(self, prev_node, msg, msg_type):
        mssg_events = list()  # list of all send_msg events
        for node_id in self.neighbours:
            if prev_node == node_id:
                continue

            receiver = self.network[node_id]
            event = self.env.process(self.send_msg(msg, receiver, msg_type))
            mssg_events.append(event)

        yield self.env.all_of(mssg_events)

    def send_msg(self, msg, receiver, msg_type):
        if msg_type == "txn":
            msg_size = 1  # in KB
        elif msg_type == "block":
            msg_size = msg.size

        delay = self.compute_delay(msg_size, receiver)
        yield self.env.timeout(delay)
        self.env.process(receiver.recv_msg(self, msg, msg_type))

    def recv_msg(self, sender, msg, msg_type):
        if msg_type == "txn":
            if msg in self.txn_pool:
                return

            self.txn_pool.append(msg)
        elif msg_type == "block":
            if msg.miner_id == self.id or self.blockchain.block_exist(msg, None):
                return

            # Check txns are valid or not
            temp_balance = self.balance.copy()
            for txn in msg.txns:
                if type(txn) is CoinbaseTransaction:
                    continue

                if temp_balance[txn.sender_id] >= txn.qty:
                    temp_balance[txn.sender_id] -= txn.qty
                    temp_balance[txn.receiver_id] += txn.qty
                    continue

                return  # block is invalid

            self.balance = temp_balance.copy()
            self.balance[msg.miner_id] += 50
            self.blockchain.add_block(msg)
            self.env.process(self.mine_block())

        print(
            f"{msg_type} received: {msg} Time: {self.env.now} Sender: {sender.id} Receiver: {self.id}"
        )
        yield self.env.process(self.broadcast_mssg(sender, msg, msg_type))
