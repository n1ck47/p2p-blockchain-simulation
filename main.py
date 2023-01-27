import simpy
from node import Node

env = simpy.Environment()
sender = Node(1, env)
receiver = Node(2, env)

env.process(sender.send_msg("hiiii", receiver))
env.run()

print(sender.prop_delay)
print(receiver.prop_delay)