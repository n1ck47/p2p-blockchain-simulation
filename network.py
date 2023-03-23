import random

# connect the nodes
def create_network(network, next_elms, que, adv_neighbors):

    visited = [False for i in range(len(network))]
    n = len(network)
    while que:
        links = random.randint(4, 8) # set a random no of neighbors for a particular node
        next_elms = random.sample(next_elms, len(next_elms)) # randomize the nodes to which the node can connect to
        u = que.pop(0)
        visited[u] = True
        if u==0:
            links = int((n-1)*adv_neighbors)
        next_elms.remove(u)
        size = links - len(network[u].neighbours) # how many new neighbours can be added
        start = len(network[u].neighbours)

        i = 0
        while next_elms: # connect node to the nodes in next_elms(randomized)
            if i >= len(next_elms):
                break

            v = next_elms[i]
            if (
                len(network[v].neighbours) < links
                and len(network[u].neighbours) < links
            ):
                network[v].neighbours.append(u)
                network[u].neighbours.append(v)
                i += 1
            elif len(network[v].neighbours) < links:
                break
            elif len(network[u].neighbours) < links:
                i += 1
            else:
                break

        for i in range(start, len(network[u].neighbours)): # Add the neighbours to the queue to do the same procedure as done above
            if not visited[network[u].neighbours[i]]:
                que.append(network[u].neighbours[i])
                visited[network[u].neighbours[i]] = True

def dfs(u, network, visited):
    visited[u] = True
    for elm in network[u].neighbours:
        if not visited[elm]:
            dfs(elm, network, visited)

def is_connected(network): # check if the network is connected or not using DFS
    visited = [False for i in range(len(network))]
    dfs(0, network, visited)
    for i in range(len(visited)):
        if not visited[i]:
            return False
    return True

def reset_network(network): # remove each and every links from the network
    for i in range(len(network)):
        network[i].neighbours.clear()

def check_links(network): # check if no of neighbours of a node is atleast 4
    for i in range(1, len(network)):
        node = network[i]
        if(len(node.neighbours)<4):
            return False
    return True

def print_network(network):
    for node in network:
        print(node.neighbours)


# run create network till its connected and no of links are atleast 4 for each node
def finalise_network(n, network, adversary_neighbors):
    while not is_connected(network) or not check_links(network):
        nodes = [i for i in range(n)]
        reset_network(network)
        create_network(network, nodes, [0], adversary_neighbors)
    # print_network(network)
