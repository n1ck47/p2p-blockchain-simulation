import random
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




def create_network(network, next_elms, links, que):
    visited = [False for i in range(len(network))]
    while(que):
        links = random.randint(4,9)
        next_elms = random.sample(next_elms, len(next_elms))
        u = que.pop(0)
        visited[u] = True
        # print(u)
        # print(network)
        next_elms.remove(u)
        size = links - len(network[u])
        start = len(network[u])
        
         #random.sample(node, len(node))
        i = 0
        while(next_elms):
            if(i >= len(next_elms)):
                break
            v = next_elms[i]
            # print(next_elms ,v)
            if(len(network[v]) < links and len(network[u])<links):
                network[v].append(u)
                network[u].append(v)
                i+=1
            elif(len(network[v]) < links):
                break
            elif(len(network[u]) < links):
                i+=1
            else:
                break


        for i in range(start, len(network[u])):
            if(not visited[network[u][i]]):
                que.append(network[u][i])
                visited[network[u][i]] = True
        # print(que)


n = 100
network = [list() for i in range(n)]



def dfs(u, network, visited):
    visited[u] = True
    for elm in network[u]:
        if(not visited[elm]):
            dfs(elm, network, visited)

def is_connected(network):
    visited = [False for i in range(len(network))]
    dfs(0, network, visited)
    for i in range(len(visited)):
        if(not visited[i]):
            return False
    return True

itr = 0
while(not is_connected(network)):
    print(itr)
    itr+=1
    if(itr>1000):
        break
    nodes = [i for i in range(n)]
    create_network(network, nodes, 3, [0])

print(is_connected(network))
print(network)
