import simpy
import random
import numpy as np

class Node:
    def __init__(self, id, env, is_fast, cpu_high):
        self.id = id
        self.env = env
        self.prop_delay = np.random.uniform(10,500)
        self.is_fast = is_fast # Is node fast or slow?
        self.cpu_high = cpu_high # Does the node have a high computing powered cpu or not?

    def compute_delay(self, msg_type, receiver):
        link_speed = 5 # in Mbps
        msg_size = 1
        if(self.is_fast and receiver.is_fast):
            link_speed = 100
        if(msg_type == "txn"):
            msg_size = 1 # in KB
        
        queueing_delay = np.random.exponential((float(96))/(link_speed*1024))
        print(queueing_delay, self.prop_delay)
        return queueing_delay + self.prop_delay + (msg_size*8)/(link_speed*1024)

    def send_msg(self,msg,receiver):
        print(f"Fast: {receiver.is_fast} -- {self.compute_delay('txn', receiver)}")
        yield self.env.timeout(10)
        receiver.recv_msg(msg)
    
    def recv_msg(self,msg):
        print(f"Mssg received: {msg}")
        
    