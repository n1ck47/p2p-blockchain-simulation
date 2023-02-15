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
        self.blockchain = Blockchain(self.env, n)
        self.pending_blocks = dict()
        self.invalid_blocks = dict()
        self.count_block_generated = 0
        self.is_gen_txn = False

    # calculate the delay to transfer a message from one node to another
    def compute_delay(self, msg_size, receiver):  # msg_size in KB
        link_speed = SLOW_LINK_SPEED  # in Mbps

        if self.is_fast and receiver.is_fast:
            link_speed = FAST_LINK_SPEED

        queueing_delay = np.random.exponential((float(96)) / (link_speed * 1024))
        return queueing_delay + self.prop_delay + (msg_size * 8) / (link_speed * 1024)

    def generate_txn(self):
        while True:
            balance = self.blockchain.get_last_block().balance[self.id] # get the node balance from the last block of longest chain
            if balance == 0: 
                break

            receiver_id = self.id

            while self.id == receiver_id:
                receiver_id = random.randint(0, self.n - 1) # Get a random node to send payment to

            payment = random.randint(int(balance/2), balance * 2) # Get a random amount to pay

            if payment > balance: 
                break 

            txn = Transaction(self.env, payment, self, self.network[receiver_id]) # create a txn
            self.txn_pool.append(txn)
            delay = np.random.exponential(self.txn_time) # find the time to wait before generating a new txn

            self.env.process(self.broadcast_mssg(None, txn, "txn")) # broadcast txn to all its neighbours
            yield self.env.timeout(delay)
            
        self.is_gen_txn = False # If break condition satisfies set is_gen_txn to false

    def mine_block(self):
        while True:
            parent_block = self.blockchain.get_last_block() # last block at the start of mining
            delay = np.random.exponential(self.mining_time / self.hashing_power)
            yield self.env.timeout(delay)

            current_parent_block = self.blockchain.get_last_block() # last block at the end of mining

            # if both the last blocks are not same 
            # that means an another node has been recieved during the mining process
            # so stop the mining
            if parent_block.get_hash() != current_parent_block.get_hash(): 
                continue 

            mined_block = Block(self.env, parent_block.get_hash(), self.id)
            mined_block.txns.append(CoinbaseTransaction(self.env, self.id))
            mined_block.balance = parent_block.balance.copy() # current balance of every node
            mined_block.size += 1

            itr = 0
            while itr < len(self.txn_pool): # keep adding txn to block till block get fulled or txn pool get emptied
                if itr >= 1022 or len(self.txn_pool) == 0:
                    break

                txn = self.txn_pool.pop(0)

                if mined_block.balance[txn.sender_id] < txn.qty:
                    continue

                mined_block.balance[txn.sender_id] -= txn.qty
                mined_block.txns.append(txn)
                mined_block.size += 1
                itr += 1

            for txn in mined_block.txns: # update the balance for every node
                if type(txn) is CoinbaseTransaction:
                    mined_block.balance[self.id] += txn.fee
                else:
                    mined_block.balance[txn.receiver_id] += txn.qty
            
            self.blockchain.add_block(mined_block) # add block to the block chain
            self.count_block_generated += 1

            if(self.is_gen_txn == False): # if the current node wasn't generating txn then start as its balance has been updated
                self.env.process(self.generate_txn())

            self.env.process(self.mine_block()) # start mining again

            yield self.env.process(self.broadcast_mssg(None, mined_block, "block")) # broadcast block to all its neighbours
            break

    def broadcast_mssg(self, prev_node, msg, msg_type):
        mssg_events = list()  # list of all send_msg events
        for node_id in self.neighbours:
            if prev_node == node_id: # don't send the mssg to the node from which you have recieved the message
                continue

            receiver = self.network[node_id]
            event = self.env.process(self.send_msg(msg, receiver, msg_type)) # generate a send message event
            mssg_events.append(event) # add that event to list

        yield self.env.all_of(mssg_events) # broadcast_mssg method will get finished when all of the send message events has been processed

    def send_msg(self, msg, receiver, msg_type):
        if msg_type == "txn":
            msg_size = 1  # in KB
        elif msg_type == "block":
            msg_size = msg.size

        delay = self.compute_delay(msg_size, receiver) # find delay in transfering to a particular node
        yield self.env.timeout(delay)   
        self.env.process(receiver.recv_msg(self, msg, msg_type)) # After the delay txn has been recieved by the reciever so call recv_msg method of the reciever

    # check if block is valid or not and if it is then add to the blockchain
    def check_add_block(self, mined_block, parent_block):
        true_balance = parent_block.balance.copy() # get the node balance from the parent block

        for txn in mined_block.txns: # check if txn amount is less than equal to the balance of the sender (valid or not)
            if type(txn) is CoinbaseTransaction:
                continue

            if true_balance[txn.sender_id] >= txn.qty:
                true_balance[txn.sender_id] -= txn.qty
                continue

            self.invalid_blocks[mined_block.get_hash()] = True
            return  "invalid" # block is invalid 

        for txn in mined_block.txns: # update the true balance (what the recieved block should have)
            if type(txn) is CoinbaseTransaction:
                true_balance[txn.miner_id] += txn.fee
            else:
                true_balance[txn.receiver_id] += txn.qty

        for i in range(len(true_balance)): # if the recieved block has the balance what it should have then its valid
            if mined_block.balance[i] == true_balance[i]:
                continue 
            self.invalid_blocks[mined_block.get_hash()] = True
            return "invalid" # block is invalid

        self.blockchain.add_block(mined_block) # block is valid so add the block to the blockchain
        self.env.process(self.mine_block()) # start mining over the new block
        return "valid"

    def recv_msg(self, sender, msg, msg_type):
        if msg_type == "txn":
            # for loop less forwarding
            if msg in self.txn_pool: # if txn already exists in the pool then dont broadcast the txn ahead
                return

            self.txn_pool.append(msg)   # if the mssg is a txn then add it to the txn pool 
        elif msg_type == "block":
            
            # for loop less forwarding
            if msg.miner_id == self.id or (msg.get_hash() in self.invalid_blocks) or self.blockchain.block_exist(msg, None) or msg in self.pending_blocks:
                return

            parent_block = self.blockchain.find_prev_block(self.blockchain.genesis, msg.prev_hash)

            if parent_block is None: # if parent doesn't exist in the current blockchain then add the block to the pending blocks (as its a future block)
                self.pending_blocks[msg.prev_hash] = msg
                return
            else:
                mined_block = msg.get_copy() # create a copy of the block so they dont have the same reference (address)

                # Check txns are valid or not
                if(self.check_add_block(mined_block, parent_block) == "invalid"): # check block validity and add if valid
                    return

                # if the recieved block's child is present in pending(future) blocks
                # then add that child to the blockchain and broadcast (if its valid)
                if msg.get_hash() in self.pending_blocks: 
                    child_block = self.pending_blocks.pop(msg.get_hash())
                    parent_block = self.blockchain.find_prev_block(self.blockchain.genesis, child_block.prev_hash)
                    if(self.check_add_block(child_block.get_copy(), parent_block) == "invalid"):
                        return
                    yield self.env.process(self.broadcast_mssg(sender, child_block, msg_type))

                # if the current node wasn't generating txn then start as its balance may have been updated
                if(self.is_gen_txn == False):
                    self.env.process(self.generate_txn())

        print(
            f"{msg_type} received: {msg} Time: {self.env.now} Creation Time: {msg.timestamp} Sender: {sender.id} Receiver: {self.id}"
        )

        yield self.env.process(self.broadcast_mssg(sender, msg, msg_type)) # broadcast the mssg to all its neighbours
