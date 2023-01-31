import simpy
from node import Node
from network import finalise_network
import numpy as np

def initialize_nodes(n, z0, z1):
    network = list()

    slow_peers = 0
    low_cpu_peers = 0

    for i in range(n):
        speed_threshold = np.random.uniform(0,1)
        cpu_threshold = np.random.uniform(0,1)
        is_fast, cpu_high = True, True
        if(speed_threshold <= z0):  # cdf (x<=z0) prob is z0
            is_fast = False
            slow_peers+=1
        if(cpu_threshold <= z1): # cdf (x<=z1) prob is z1
            cpu_high = False
            low_cpu_peers += 1
        node = Node(i, env, is_fast, cpu_high)
        network.append(node)

    fast_peers = n - slow_peers
    high_cpu_peers = n - low_cpu_peers

    set_hashing_power(low_cpu_peers, high_cpu_peers, network)

    return network

def set_hashing_power(low_cpu_peers, high_cpu_peers, network):
    low_hash_power = 1/(low_cpu_peers + 10*high_cpu_peers)
    high_hash_power = 10*low_hash_power
    
    for i in range(len(network)):
        if(network[i].cpu_high):
            network[i].hashing_power = high_hash_power
        else:
            network[i].hashing_power = low_hash_power

# def run_txns():


env = simpy.Environment()
n = 10 # number of peers
z0 = 0.4 # Fraction of slow peers
z1 = 0.4 # Fraction of low cpu peers

Node.network = initialize_nodes(n, z0, z1)
finalise_network(n,Node.network) # connects the peers 

for node in Node.network:
    env.process(node.generate_txn())
env.run()

# for elm in Node.network:
#     print(elm.neighbours, elm.txn_pool, len(elm.txn_pool))

for node in Node.network:
    print(node.balance)
