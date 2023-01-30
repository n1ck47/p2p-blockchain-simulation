import random
network=list()
network.extend([0,1.2])
adj_list=dict()     #adjacency list of a network
adj_list[0]=[1]
adj_list[1]=[0]
adj_list[2]=[]
visited=[False]*len(adj_list)
def dfs(node):     #dfs to check if graph is connected
    if visited[node] is True:
        return
    else:
        visited[node]=True
        for i in adj_list[node]:
            if visited[i] is False:
                dfs(node)
def is_connected():   #method to check if graph is connected
    dfs(0)
    for i in adj_list.keys():
        if visited[i] is False:
            return False
    return True

while(not is_connected()):  #while graph is not connected arrange 
    print("Iteration")
    length=len(adj_list)
    fro = random.randint(0,length)
    to = random.randint(0,length)
    if fro==to:
        continue
    else:
        adj_list[fro]=to
        adj_list[to]=fro
print("Done")