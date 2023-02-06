import queue

from block import GenesisBlock


class Blockchain:
    def __init__(self, n):
        self.genesis = GenesisBlock(n)
        self.total = 1

    def height(self, node):
        if node is None:
            return (0, None)

        if len(node.children) == 0:
            return (1, node)
        else:
            heights = [self.height(child) for child in node.children]
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, last_block)

    def find_prev_block(self, node, prevhash):
        if node is None:
            return None

        if node.get_hash() == prevhash:
            return node
        else:
            for child in node.children:
                result = self.find_prev_block(child, prevhash)
                if result:
                    return result

            return None

    def get_last_block(self):
        finalblock = self.height(self.genesis)[1]

        return finalblock

    def add_block(self, block):
        if block is None:
            return

        new_block = block.get_copy()
        prevhash = block.prev_hash
        prevblock = self.find_prev_block(self.genesis, prevhash)
        if prevblock is None:
            return

        prevblock.children.append(new_block)

    def block_exist(self, block, current_block):
        if current_block is None:
            current_block = self.genesis

        if block is None:
            return None
            
        if block.get_hash() == current_block.get_hash():
            return True

        for child in current_block.children:
            if self.block_exist(block, child):
                return True

        return False

    def all_nodes_in_chain(self, node):
        if not node.children:
            return (1, [node])

        else:
            heights = [self.all_nodes_in_chain(child) for child in node.children]
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, [node] + last_block)

    def display_chain(self):
        return [node.get_hash() for node in self.all_nodes_in_chain(self.genesis)[1]]

    def get_blockchain_tree(self):
        adjancency_list = {}
        block = self.genesis
        blocks_queue = queue.Queue()
        blocks_queue.put(self.genesis)

        while not blocks_queue.empty():
            block = blocks_queue.get()
            adjancency_list[f"{str(block.id)}::{str(block.timestamp)}"] = [f"{str(i.id)}::{str(i.timestamp)}" for i in block.children]

            for bl in block.children:
                blocks_queue.put(bl)

        return adjancency_list
