import os

import pydot
from treelib import Tree            #Used treelib and graphviz for visualization

from constants import *

files = []

for fname in os.listdir(TREE_OUTPUT_DIR):
    files.append(fname)
    
files.sort()

for fname in files:             #Reading each file of a node and generating the blockchain for that node
    if TREE_OUTPUT_FILE_PREFIX in fname and "txt" not in fname:
        continue

    BLOCK_NODE_MAPPING = {}

    print(f"Visualizing :: {fname}")
    tree = Tree()
    with open(f"{TREE_OUTPUT_DIR}/{fname}") as f:
        lines = [i.strip() for i in f.readlines()]

    node_counter = 0

    root_node = lines[0].split()[0].split("::")[0]
    BLOCK_NODE_MAPPING[root_node] = lines[0].split()[0].split("::")[2]

    tree.create_node(str(node_counter), root_node, data="-1")
    node_counter += 1
    for l in lines:
        nodes = l.split()
        for n in range(1, len(nodes)):
            miner_id = nodes[n].split("::")[2]
            block_id = nodes[n].split("::")[0]
            BLOCK_NODE_MAPPING[block_id] = miner_id
            tree.create_node(str(node_counter), block_id, parent=nodes[0].split("::")[0], data=str(miner_id))
            node_counter += 1
    

    tree.to_graphviz("graph.txt")

    # editing graph.txt to include color

    with open("graph.txt") as f_graph:
        lines = [i.strip() for i in f_graph.readlines()]
    
    updated_graph_txt = []

    for line in lines:
        if "label" in line and "shape" in line:
            block_id = line.split('"')[1]
            if BLOCK_NODE_MAPPING[block_id] == "0":
                updated_line = line[:-1] + ', style="filled", fillcolor="red"]'
                updated_graph_txt.append(updated_line)
            else:
                updated_graph_txt.append(line)
        else:
            updated_graph_txt.append(line)

    with open("graph.txt", "w") as f_graph:
        f_graph.writelines(updated_graph_txt)

    dot = pydot.graph_from_dot_file("graph.txt")
    os.remove("graph.txt")

    output_fname = fname.split(".")[0] + ".png"
    dot[0].write_png(f"{TREE_OUTPUT_DIR}/{output_fname}")
