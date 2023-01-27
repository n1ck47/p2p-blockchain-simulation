import simpy
from node import Node

env = simpy.Environment()
n = 10
network = list()
for i in range(n):
    node = Node(i, env, True, True)
    network.append(node)

env.process(network[2].send_msg("hiiii", network[5]))
env.process(network[4].send_msg("hiiii", network[9]))
env.run()

