import random


def create_network(network, next_elms, que):
    visited = [False for i in range(len(network))]

    while que:
        links = random.randint(4, 8)
        next_elms = random.sample(next_elms, len(next_elms))
        u = que.pop(0)
        visited[u] = True
        next_elms.remove(u)
        size = links - len(network[u].neighbours)
        start = len(network[u].neighbours)

        i = 0
        while next_elms:
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

        for i in range(start, len(network[u].neighbours)):
            if not visited[network[u].neighbours[i]]:
                que.append(network[u].neighbours[i])
                visited[network[u].neighbours[i]] = True


def dfs(u, network, visited):
    visited[u] = True
    for elm in network[u].neighbours:
        if not visited[elm]:
            dfs(elm, network, visited)


def is_connected(network):
    visited = [False for i in range(len(network))]
    dfs(0, network, visited)
    for i in range(len(visited)):
        if not visited[i]:
            return False
    return True


def finalise_network(n, network):
    while not is_connected(network):
        nodes = [i for i in range(n)]
        create_network(network, nodes, [0])
