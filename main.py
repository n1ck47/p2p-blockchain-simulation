import simpy
from node import Node
from network import finalise_network
import numpy as np
from pathlib import Path
from constants import *

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

for elm in Node.network:
    print(elm.id, elm.neighbours)

for node in Node.network:
    env.process(node.generate_txn())
    env.process(node.mine_block())

env.run(until=301180)

# for elm in Node.network:
#     print(elm.id, len(elm.txn_pool))

for node_i in range(len(Node.network)):
    node = Node.network[node_i]
    print(node.id, len(node.blockchain.display_chain()))

    Path(TREE_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    adj = node.blockchain.get_blockchain_tree()

    with open(f'{TREE_OUTPUT_DIR}/{TREE_OUTPUT_FILE_PREFIX}{node_i}.txt', 'w') as f:
        for i in adj:

            pr_str = i
            for j in adj[i]:
                pr_str += f" {j}"
            
            pr_str += "\n"
            
            f.write(pr_str)
