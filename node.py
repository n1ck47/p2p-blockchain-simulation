import simpy
import random
import numpy as np
from txn import Transaction, CoinbaseTransaction
from functools import reduce
from block import Block
from blockchain import Blockchain

class Node:
    network = list()
    txn_time = 6000 # avg interarrival time between each txn generation
    mining_time = 600000
    def __init__(self, id, env, is_fast, cpu_high):
        self.id = id
        self.env = env
        self.prop_delay = np.random.uniform(10,500)
        self.is_fast = is_fast # Is node fast or slow?
        self.cpu_high = cpu_high # Does the node have a high computing powered cpu or not?
        self.neighbours = list()
        self.hashing_power = 0
        self.txn_pool = list()
        self.utx0 = list()
        self.balance = 1000
        self.mining_money = 0
        self.blockchain = Blockchain()

    def update_balance(self):
        self.balance = 0
        for txn in self.utx0:
            self.balance += txn.qty

    def compute_delay(self, msg_size, receiver): # msg_size in KB
        link_speed = 5 # in Mbps
        if(self.is_fast and receiver.is_fast):
            link_speed = 100
        
        queueing_delay = np.random.exponential((float(96))/(link_speed*1024))
        return queueing_delay + self.prop_delay + (msg_size*8)/(link_speed*1024)

    def generate_txn(self):
        itr=0
        while True:
            txn = str(self.id)+"Hellu"+str(len(self.txn_pool)) #create txn object
            n = len(self.network)
            receiver_id = self.id
            while(self.id == receiver_id):
                receiver_id = random.randint(0, n-1)

            # print(receiver_id ,len(self.network))
            txn = Transaction(100, self, self.network[receiver_id])
            self.txn_pool.append(txn)
            delay = np.random.exponential(self.txn_time)
            self.env.process(self.broadcast_mssg(None, txn, 'txn')) 
            yield self.env.timeout(delay)
            itr+=1
            if(itr>20):
                break
            
            

    def mine_block(self):
        while True:
            parent_block = self.blockchain.getlastblock()
            delay = np.random.exponential(self.mining_time / self.hashing_power)
            yield self.env.timeout(delay)
            current_parent_block = self.blockchain.getlastblock()

            if(parent_block.get_hash() != current_parent_block.get_hash()):
                continue

            mined_block = Block(parent_block.get_hash(), self.id)
            mined_block.txns.append(CoinbaseTransaction(self.id))
            mined_block.size += 1

            # print(type(mined_block.txns[0]) is CoinbaseTransaction)
            
            for i in range(len(self.txn_pool)):
                if(i>=1022):
                    break
                mined_block.txns.append(self.txn_pool.pop(0))
                mined_block.size += 1
            # print()
            # print()
            # print(f'MINED {mined_block.get_hash()}')
            self.mining_money += 50
            # print()
            # print()

            # for node in self.network:
            #     print(node.id, node.blockchain.display_chain())
            # print()

            self.blockchain.add_block(mined_block)

            # for node in self.network:
            #     print(node.blockchain, 'aaaa')
            #     print(node.id, node.blockchain.display_chain())
            # print()
            self.env.process(self.mine_block())
            yield self.env.process(self.broadcast_mssg(None, mined_block, 'block')) 
            break

    def broadcast_mssg(self, prev_node, msg, msg_type):
        mssg_events = list() # list of all send_msg events
        for node_id in self.neighbours:
            if(prev_node == node_id):
                continue
            receiver = self.network[node_id]
            event =  self.env.process(self.send_msg(msg, receiver, msg_type))
            mssg_events.append(event)

        yield self.env.all_of(mssg_events) 

    def send_msg(self,msg,receiver, msg_type):
        if(msg_type == 'txn'):
            msg_size = 1 # in KB
        elif(msg_type == 'block'):
            msg_size = msg.size
        delay = self.compute_delay(msg_size, receiver)
        yield self.env.timeout(delay)
        self.env.process(receiver.recv_msg(self, msg, msg_type))
        # return delay        
    
    def recv_msg(self,sender, msg, msg_type):
        
        if(msg_type == 'txn'):
            if msg in self.txn_pool:
                return
            self.txn_pool.append(msg)
            if(msg.receiver_id == self.id):
                self.utx0.append(msg)
                self.update_balance()
        elif(msg_type == 'block'):
            # print(self.id, self.blockchain.display_chain())
            # print('aaa0', self.blockchain.block_exist(msg, None))
            if msg.miner_id == self.id or self.blockchain.block_exist(msg, None):
                return
            # Check txns are valid or not
            for txn in msg.txns:
                if(type(txn) is CoinbaseTransaction):
                    continue
                temp_sender = self.network[txn.sender_id]
                if(temp_sender.balance >= txn.qty):
                    continue
                return # block is invalid

            for txn in msg.txns:
                if(type(txn) is CoinbaseTransaction):
                    continue
                self.txn_pool.remove(txn)
            self.blockchain.add_block(msg)

            # print(f"{msg_type} received: {msg} Time: {self.env.now} Sender: {sender.id} Receiver: {self.id}")
            # print(re)
            # print(self.blockchain.display_chain())
            self.env.process(self.mine_block())
        yield self.env.process(self.broadcast_mssg(sender, msg, msg_type))