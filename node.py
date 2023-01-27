import simpy
import random
import numpy as np

class Node:
    def __init__(self, id, env):
        self.id = id
        self.env = env
        self.prop_delay = np.random.uniform(10,500)

    

    def send_msg(self,msg,receiver):

        yield self.env.timeout(10)
        receiver.recv_msg(msg)
    
    def recv_msg(self,msg):
        print(f"Mssg received: {msg}")
        

