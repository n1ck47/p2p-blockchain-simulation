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

    def compute_delay(self, msg_size, receiver):
        link_speed = 5 # in Mbps
        msg_size = 1
        if(self.is_fast and receiver.is_fast):
            link_speed = 100
        
        queueing_delay = np.random.exponential((float(96))/(link_speed*1024))
        return queueing_delay + self.prop_delay + (msg_size*8)/(link_speed*1024)

    def generate_txn(self):
        itr = 0
        while True:
            txn = str(self.id)+"Hellu"+str(len(self.txn_pool)) #create txn object
            self.txn_pool.append(txn)
            yield self.env.process(self.broadcast_txn(None, txn))
            itr+=1
            if(itr>5):
                break

    def broadcast_txn(self, prev_node, txn):
        mssg_events = list() # list of all send_msg events
        for node_id in self.neighbours:
            if(prev_node == node_id):
                continue
            receiver = self.network[node_id]
            event =  self.env.process(self.send_msg(txn, receiver, 'txn'))
            mssg_events.append(event)

        yield self.env.all_of(mssg_events) 

    def send_msg(self,msg,receiver, msg_type):
        if(msg_type == 'txn'):
            msg_size = 1 # in KB
            delay = self.compute_delay(msg_size, receiver)
            yield self.env.timeout(delay)
            self.env.process(receiver.recv_msg(self, msg, msg_type))
            return delay
            
    
    def recv_msg(self,sender, msg, msg_type):
        if(msg_type == 'txn'):
            if msg in self.txn_pool:
                return
            self.txn_pool.append(msg)
            print(f"Mssg received: {msg} Time: {self.env.now} Sender: {sender.id} Receiver: {self.id}")
        
        yield self.env.process(self.broadcast_txn(sender, msg))