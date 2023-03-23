import sys
import shutil
import numpy as np
import simpy
from tabulate import tabulate


from constants import *
from network import finalise_network
from node import Node
from blockchain import Blockchain


import os
import sys
sys.setrecursionlimit(100000)


# create nodes and initialize them with their hashing power
# and label them with fast/slow and high/low cpu
def initialize_nodes(n, z0, z1, env, txn_time, mining_time, adv_mining_power):
    network = list()

    slow_peers = 0
    low_cpu_peers = 0

    #intializing adversary
    node = Node(0, env, True, True, n, txn_time, mining_time)
    network.append(node)

    z1 = (n*z1)/(n-1)
    
    for i in range(1, n):
        speed_threshold = np.random.uniform(0, 1)
        cpu_threshold = np.random.uniform(0, 1)
        is_fast, cpu_high = True, True

        # z0 is the prob that a node is slow
        if speed_threshold <= z0: 
            is_fast = False
            slow_peers += 1

        # z1 is the prob that a node has low cpu
        if cpu_threshold <= z1:
            cpu_high = False
            low_cpu_peers += 1

        node = Node(i, env, is_fast, cpu_high, n, txn_time, mining_time)
        network.append(node)

    fast_peers = n - slow_peers
    high_cpu_peers = n - low_cpu_peers

    set_hashing_power(low_cpu_peers, high_cpu_peers, network, adv_mining_power)

    return network

# set hasing power for a high and low cpu node
def set_hashing_power(low_cpu_peers, high_cpu_peers, network, adv_mining_power):
    high_cpu_peers -= 1 # removing adversary
    low_hash_power = (1  - adv_mining_power )/ (low_cpu_peers + 10 * high_cpu_peers)
    high_hash_power = 10 * low_hash_power

    for i in range(len(network)):
        if i == 0:
            network[i].hashing_power = adv_mining_power
            continue
        if network[i].cpu_high:
            network[i].hashing_power = high_hash_power
        else:
            network[i].hashing_power = low_hash_power

def main(n, z0, z1, txn_time, mining_time, simulation_until, adv_mining_power, adversary_neighbors, do_selfish_mining):

    env = simpy.Environment()

    Node.attack_type = do_selfish_mining
    # if Node.network is None: 
    Node.network = initialize_nodes(n, z0, z1, env, txn_time, mining_time, adv_mining_power)
    finalise_network(n, Node.network, adversary_neighbors)  # connects the peers
    # else:
    #     for i in range(len(Node.network)):
    #         Node.network[i].env = env
    #         Node.network[i].txn_pool = list()
    #         Node.network[i].blockchain = Blockchain(env, n)
    #         Node.network[i].pending_blocks = dict()
    #         Node.network[i].invalid_blocks = dict()
    #         Node.network[i].count_block_generated = 0
    #         Node.network[i].is_gen_txn = False
    #         Node.network[i].attacked_block = None
    #         Node.network[i].is_selfish_mining = False
    #         Node.network[i].is_stubborn_mining = False


    for node in Node.network:
        env.process(node.generate_txn()) # add generate txn event to the simpy environment
        node.is_gen_txn = True
        env.process(node.mine_block()) # add mine block event to the simpy environment

    env.run(until=simulation_until) # run the simulation

    if os.path.exists(TREE_OUTPUT_DIR):
        shutil.rmtree(TREE_OUTPUT_DIR)
    os.mkdir(TREE_OUTPUT_DIR)

    output = list()
    no_blocks_main_chain = len(Node.network[0].blockchain.display_chain())
    total_blocks_gen = Node.network[0].blockchain.blocks_count()
    mpu_adv = 0
    adv_block_main = 0
    r_pool = 0
    # Formatting and saving trees of all nodes in txt files
    for node_i in range(len(Node.network)):
        node = Node.network[node_i]
        # print(node.id, len(node.blockchain.display_chain()), len(node.pending_blocks),node.blockchain.get_last_block().balance)
        
        # print(f'Node: {node.id}, Mined Blocks(Chain/Generated): {node.blockchain.count_mined_block(node.id)}/{node.count_block_generated}, Total Blocks: {len(node.blockchain.display_chain())}, Fast?: {node.is_fast}, Cpu High?: {node.cpu_high}')
        # print(Node.network[node.id])
        # no_blocks_main_chain = max(no_blocks_main_chain,len(node.blockchain.display_chain()))
        node_no = str(node.id)
        if node.id == 0:
            node_no += " (Adversary)"
            adv_block_main = node.blockchain.count_mined_block(node.id)
            if node.count_block_generated:
                mpu_adv = float(adv_block_main)/node.count_block_generated
        output.append([node_no, str(node.blockchain.count_mined_block(node.id))+":"+str(node.count_block_generated), no_blocks_main_chain, node.is_fast, node.cpu_high, node.hashing_power])
        
        # total_blocks_gen += node.count_block_generated
        adj = node.blockchain.get_blockchain_tree()

        with open(f"{TREE_OUTPUT_DIR}/{TREE_OUTPUT_FILE_PREFIX}{node_i}.txt", "w") as f:
            for i in adj:

                pr_str = i
                for j in adj[i]:
                    pr_str += f" {j}"

                pr_str += "\n"

                f.write(pr_str)

    
    header = ["Node", " Mined Blocks(Chain:Generated)", "Total Blocks", "Fast?", "Cpu High?", "Hashing power"]
    
    # ouput table 
    # print(tabulate(output, headers=header, tablefmt="grid"))
    mpu_overall = 0
    if total_blocks_gen:
        mpu_overall = float(no_blocks_main_chain)/total_blocks_gen
    if no_blocks_main_chain:
        r_pool = float(adv_block_main)/(no_blocks_main_chain)
    # print(f"R_pool: {r_pool}")
    return mpu_adv, mpu_overall
    # print(f"MPU Adversary: {mpu_adv}\nMPU Overall: {mpu_overall}")
    # print(f"No of blocks in the main chain: {no_blocks_main_chain}")
    # print(f"Total blocks generated: {total_blocks_gen}")
    

# Take parameters from the command line
if __name__ == "__main__":
    args = len(sys.argv)

    # if args < 9 or args > 9 or ( sys.argv[8]!='0' and sys.argv[8]!='1' ):
    #     print(
    #         "Provide 8 arguments:\n"
    #         "No. of nodes\n"
    #         "Adversary mining power\n"
    #         "No of adversary's neighbors\n"
    #         "Fraction of low cpu peers\n"
    #         "Transaction time in ms\n"
    #         "Mining time in ms\n"
    #         "Simulation time units\n"
    #         "Selfish mining?(1/0)"
    #     )
    #     exit(1)

    # n = int(sys.argv[1])  # no. of peers
    # z0 = 0.5  # fraction of slow peers
    # adv_mining_power = float(sys.argv[2])
    # adversary_neighbors = float(sys.argv[3])
    # z1 = float(sys.argv[4])  # fraction of low cpu peers
    # txn_time = int(sys.argv[5])  # transaction time (interarrival time) in ms
    # mining_time = int(sys.argv[6])  # mining time in ms
    # simulation_until = int(sys.argv[7]) # simulation time
    # do_selfish_mining = int(sys.argv[8]) # do selfish mining
    # main(n, z0, z1, txn_time, mining_time, simulation_until, adv_mining_power, adversary_neighbors, do_selfish_mining)

    n = 50  # no. of peers
    z0 = 0.5  # fraction of slow peers
    z1 = 0.3  # fraction of low cpu peers
    txn_time = 1000  # transaction time (interarrival time) in ms
    mining_time = 6000  # mining time in ms
    simulation_until = 100000 # simulation time
    do_selfish_mining = 1 # do selfish mining

    print("Alpha, Gamma, Expected Result, Test Result Selfish, Test result stuborn")
    for i in range(5,61,5):
        adv_mining_power = i/100
        for j in range(10,101,15):
            adversary_neighbors = j/100
            alpha = adv_mining_power
            gamma = adversary_neighbors
            num=alpha*((1-alpha)**2)*(4*alpha+gamma*(1-2*alpha))-alpha**3
            den=1-alpha*(1+(2-alpha)*alpha)
            selfish_result = main(n, z0, z1, txn_time, mining_time, simulation_until, adv_mining_power, adversary_neighbors, do_selfish_mining)
            # Node.network = None
            stubborn_result = main(n, z0, z1, txn_time, mining_time, simulation_until, adv_mining_power, adversary_neighbors, 0)
            Node.network = None
            print(f"{alpha}, {gamma}, {selfish_result}, {stubborn_result}")