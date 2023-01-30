import simpy
import random
import numpy as np

class Node:
    network = list()
    def __init__(self, id, env, is_fast, cpu_high):
        self.id = id
        self.env = env
        self.prop_delay = np.random.uniform(10,500)
        self.is_fast = is_fast # Is node fast or slow?
        self.cpu_high = cpu_high # Does the node have a high computing powered cpu or not?
        self.neighbours = list()
        self.hashing_power = 0
        self.txn_pool = list()

    def compute_delay(self, msg_type, receiver):
        link_speed = 5 # in Mbps
        msg_size = 1
        if(self.is_fast and receiver.is_fast):
            link_speed = 100
        if(msg_type == "txn"):
            msg_size = 1 # in KB
        
        queueing_delay = np.random.exponential((float(96))/(link_speed*1024))
        # print(queueing_delay, self.prop_delay)
        return queueing_delay + self.prop_delay + (msg_size*8)/(link_speed*1024)

    def generate_txn(self):
        txn = "Hellu" #create txn object
        self.txn_pool.append(txn)
        for node_id in self.neighbours:
            receiver = self.network[node_id]
            self.env.process(self.send_msg(txn, receiver))
        yield self.env.timeout(0)

    def send_msg(self,msg,receiver):
        delay = self.compute_delay('txn', receiver)
        # print(f"Sender: {self.id} Receiver: {receiver.id}")
        # print(f"High: {receiver.cpu_high} -- Delay: {delay} -- Power: {self.hashing_power}")
        yield self.env.timeout(delay)
        self.env.process(receiver.recv_msg(self, msg))
    
    def recv_msg(self,sender, msg):
        if msg in self.txn_pool:
            return
        self.txn_pool.append(msg)
        print(f"Mssg received: {msg} Time: {self.env.now} Sender: {sender.id} Receiver: {self.id}")
        
        for node_id in self.neighbours:
            if sender == node_id:
                continue
            receiver = self.network[node_id]
            self.env.process(self.send_msg(msg, receiver))
        yield self.env.timeout(0)