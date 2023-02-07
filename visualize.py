import os

import pydot
from treelib import Tree

from constants import *

for fname in os.listdir(TREE_OUTPUT_DIR):
    if TREE_OUTPUT_FILE_PREFIX in fname and "txt" not in fname:
        continue
    print(f"Visualizing :: {fname}")
    tree = Tree()
    with open(f"{TREE_OUTPUT_DIR}/{fname}") as f:
        lines = [i.strip() for i in f.readlines()]

    node_counter = 0

    root_node = lines[0].split()[0].split("::")[0]

    tree.create_node(str(node_counter), root_node)
    node_counter += 1
    for l in lines:
        nodes = l.split()
        for n in range(1, len(nodes)):
            tree.create_node(str(node_counter), nodes[n].split("::")[0], parent=nodes[0].split("::")[0])
            node_counter += 1

    tree.to_graphviz("graph.txt")
    dot = pydot.graph_from_dot_file("graph.txt")
    os.remove("graph.txt")

    output_fname = fname.split(".")[0] + ".png"
    dot[0].write_png(f"{TREE_OUTPUT_DIR}/{output_fname}")
