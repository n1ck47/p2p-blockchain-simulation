import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

G = nx.Graph()
adjacency_list =dict()
adjacency_list["nodes"]=[]
adjacency_list["links"]=[]
with open("graph.txt") as gr:
    for block in gr:
        curr= block.split()[0]
        adjacency_list["nodes"].append({"id":curr, "name":curr})
        child= block.split()[1:]
        for i in child:
            adjacency_list["links"].append({"source":curr, "target":i})
        # adjacency_list.update({ block: { e: 1 for e in block[1:] } })
print(adjacency_list)
graph_json=adjacency_list
# nx.draw_shell(G, with_labels = True, node_color = "c", edge_color = "k", font_size = 8, style='dashed')
# #nx.line_graph(G)
# plt.axis('off')
# plt.draw()
# plt.savefig("graph.pdf")
node_labels = {node['id']:node['name'] for node in graph_json['nodes']}
for n in graph_json['nodes']:
    del n['name']
g = json_graph.node_link_graph(graph_json, directed=True, multigraph=False)
pos = graphviz_layout(g, prog="dot")
nx.draw(g.to_directed(), pos, labels=node_labels, with_labels=True)
plt.show()
