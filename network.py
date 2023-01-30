# import random
# network=list()
# network.extend([0,1.2])
# adj_list=dict()     #adjacency list of a network
# adj_list[0]=[1]
# adj_list[1]=[0]
# adj_list[2]=[]
# visited=[False]*len(adj_list)
# def dfs(node):     #dfs to check if graph is connected
#     if visited[node] is True:
#         return
#     else:
#         visited[node]=True
#         for i in adj_list[node]:
#             if visited[i] is False:
#                 dfs(node)
# def is_connected():   #method to check if graph is connected
#     dfs(0)
#     for i in adj_list.keys():
#         if visited[i] is False:
#             return False
#     return True

# while(not is_connected()):  #while graph is not connected arrange 
#     print("Iteration")
#     length=len(adj_list)
#     fro = random.randint(0,length)
#     to = random.randint(0,length)
#     if fro==to:
#         continue
#     else:
#         adj_list[fro]=to
#         adj_list[to]=fro
# print("Done")
import random

def is_connected(graph, node, visited):
  visited.add(node)
  for neighbor in graph[node]:
    if neighbor not in visited:
      is_connected(graph, neighbor, visited)

def random_connections(nodes, min_conn, max_conn):
    while True:
        graph = {node: set() for node in nodes}
        for node in graph:
            targets = list(set(nodes) - set([node]- set(graph[node])))
            random.shuffle(list(targets))
            targets = targets[:min(max_conn, len(targets))]
            for target in targets:
                graph[node].add(target)
                graph[target].add(node)
        visited = set()
        is_connected(graph, list(graph.keys())[0], visited)
        if len(visited) == len(graph):
            break
    return graph

nodes = [i for i in range(100)]
graph = random_connections(nodes, 4, 8)
print(graph)