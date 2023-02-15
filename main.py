import sys
import shutil
import numpy as np
import simpy
from tabulate import tabulate


from constants import *
from network import finalise_network
from node import Node

import os
import sys
sys.setrecursionlimit(100000)


def initialize_nodes(n, z0, z1, env, txn_time, mining_time):
    network = list()

    slow_peers = 0
    low_cpu_peers = 0

    for i in range(n):
        speed_threshold = np.random.uniform(0, 1)
        cpu_threshold = np.random.uniform(0, 1)
        is_fast, cpu_high = True, True

        if speed_threshold <= z0:  # cdf (x<=z0) prob is z0
            is_fast = False
            slow_peers += 1

        if cpu_threshold <= z1:  # cdf (x<=z1) prob is z1
            cpu_high = False
            low_cpu_peers += 1

        node = Node(i, env, is_fast, cpu_high, n, txn_time, mining_time)
        network.append(node)

    fast_peers = n - slow_peers
    high_cpu_peers = n - low_cpu_peers

    set_hashing_power(low_cpu_peers, high_cpu_peers, network)

    return network


def set_hashing_power(low_cpu_peers, high_cpu_peers, network):
    low_hash_power = 1 / (low_cpu_peers + 10 * high_cpu_peers)
    high_hash_power = 10 * low_hash_power

    for i in range(len(network)):
        if network[i].cpu_high:
            network[i].hashing_power = high_hash_power
        else:
            network[i].hashing_power = low_hash_power


def main(n, z0, z1, txn_time, mining_time, simulation_until):

    env = simpy.Environment()

    Node.network = initialize_nodes(n, z0, z1, env, txn_time, mining_time)
    finalise_network(n, Node.network)  # connects the peers

    # for elm in Node.network:
    #     print(elm.id, elm.neighbours)

    for node in Node.network:
        env.process(node.generate_txn())
        env.process(node.mine_block())

    env.run(until=simulation_until)

    if os.path.exists(TREE_OUTPUT_DIR):
        shutil.rmtree(TREE_OUTPUT_DIR)
    os.mkdir(TREE_OUTPUT_DIR)

    output = list()
    total_blocks_gen = 0
    for node_i in range(len(Node.network)):
        node = Node.network[node_i]
        # print(node.id, len(node.blockchain.display_chain()), len(node.pending_blocks),node.blockchain.get_last_block().balance)
        
        # print(f'Node: {node.id}, Mined Blocks(Chain/Generated): {node.blockchain.count_mined_block(node.id)}/{node.count_block_generated}, Total Blocks: {len(node.blockchain.display_chain())}, Fast?: {node.is_fast}, Cpu High?: {node.cpu_high} Balance: {sum(node.blockchain.get_last_block().balance)}')

        output.append([node.id, str(node.blockchain.count_mined_block(node.id))+":"+str(node.count_block_generated), len(node.blockchain.display_chain()), node.is_fast, node.cpu_high])

        total_blocks_gen += node.count_block_generated
        adj = node.blockchain.get_blockchain_tree()

        with open(f"{TREE_OUTPUT_DIR}/{TREE_OUTPUT_FILE_PREFIX}{node_i}.txt", "w") as f:
            for i in adj:

                pr_str = i
                for j in adj[i]:
                    pr_str += f" {j}"

                pr_str += "\n"

                f.write(pr_str)

    header = ["Node", " Mined Blocks(Chain:Generated)", "Total Blocks", "Fast?", "Cpu High?"]
    
    print()
    print(tabulate(output, headers=header, tablefmt="grid"))
    print(f"Total block generated: {total_blocks_gen}")
    print()


if __name__ == "__main__":
    args = len(sys.argv)

    if args < 7 or args > 7:
        print(
            "Provide 5 arguments:\n"
            "No. of nodes\n"
            "Fraction of slow peers\n"
            "Fraction of low cpu peers\n"
            "Transaction time in ms\n"
            "Mining time in ms\n"
            "Simulation time units"
        )
        exit(1)

    n = int(sys.argv[1])  # no. of peers
    z0 = float(sys.argv[2])  # fraction of slow peers
    z1 = float(sys.argv[3])  # fraction of low cpu peers
    txn_time = int(sys.argv[4])  # transaction time (interarrival time) in ms
    mining_time = int(sys.argv[5])  # mining time in ms
    simulation_until = int(sys.argv[6])

    main(n, z0, z1, txn_time, mining_time, simulation_until)
