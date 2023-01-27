import simpy
from node import Node
import numpy as np

env = simpy.Environment()
n = 10
z0 = 0.4 # Fraction of slow peers
z1 = 0.2 # Fraction of low cpu peers
network = list()
for i in range(n):
    speed_threshold = np.random.uniform(0,1)
    cpu_threshold = np.random.uniform(0,1)
    is_fast, cpu_high = True, True
    if(speed_threshold <= z0):
        is_fast = False
    if(cpu_threshold <= z1):
        cpu_high = False
    node = Node(i, env, is_fast, cpu_high)
    network.append(node)

env.process(network[2].send_msg("hiiii", network[5]))
env.process(network[4].send_msg("hiiii", network[9]))
env.run()

