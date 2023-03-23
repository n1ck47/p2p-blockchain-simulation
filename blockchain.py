import queue

from block import GenesisBlock


class Blockchain:               #Class for Blockchain
    def __init__(self, env, n):
        self.genesis = GenesisBlock(env, n)
        self.total = 1

    def height(self, node):       #Helper function to get last block
        if node is None:
            return (0, None)

        if len(node.children) == 0:
            return (1, node)
        else:
            heights = [self.height(child) for child in node.children]     #doing dfs for each child
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, last_block)

    def find_prev_block(self, node, prevhash):          # Method to find parent block
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

    def get_last_block(self):               #Method to get last block in longest blockchain
        finalblock = self.height(self.genesis)[1]

        return finalblock

    def blocks_count(self,block=None):
        if block is None:
            block = self.genesis
        if len(block.children)==0:
            return 1
        ans = 1
        for node in block.children:
            ans += self.blocks_count(node)
        return ans

    def add_block(self, block):         #Method to add block in blockchain
        if block is None:
            return

        new_block = block.get_copy()
        prevhash = block.prev_hash
        prevblock = self.find_prev_block(self.genesis, prevhash)        #Get the parent block using previous hash
        if prevblock is None:
            return

        prevblock.children.append(new_block)

    def block_exist(self, block, current_block):            #Method to check if block already exist in blockchain
        if current_block is None:
            current_block = self.genesis

        if block is None:
            return None

        if block.get_hash() == current_block.get_hash():     
            return True

        for child in current_block.children:                    #DFS for checking if block exist in blockchian
            if self.block_exist(block, child):
                return True

        return False

    def all_nodes_in_chain(self, node):             #Helper method to display chain
        if not node.children:
            return (1, [node])

        else:
            heights = [self.all_nodes_in_chain(child) for child in node.children]
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, [node] + last_block)

    def display_chain(self):            # Method to get final blockchain
        return [(node.id, node.get_hash()) for node in self.all_nodes_in_chain(self.genesis)[1]]

    def count_mined_block(self, node_id):       #Method to count number blocks mined
        longest_chain = self.all_nodes_in_chain(self.genesis)[1]
        count = 0
        for block in longest_chain:
            if type(block) is GenesisBlock:
                continue
            if node_id == block.miner_id:
                count+=1
        return count

    def get_blockchain_tree(self):          #Method to get blockchain with forks in the form of adjacency list.
        adjancency_list = {}
        block = self.genesis
        blocks_queue = queue.Queue()
        blocks_queue.put(self.genesis)

        while not blocks_queue.empty():
            block = blocks_queue.get()
            #Making adjacency list of blockchain to help visualizing the final blockchain
            adjancency_list[f"{str(block.id)}::{str(block.timestamp)}::{str(block.miner_id)}"] = [f"{str(i.id)}::{str(i.timestamp)}::{str(i.miner_id)}" for i in block.children] 

            for bl in block.children:
                blocks_queue.put(bl)

        return adjancency_list
    
    def helper(self,block,hash,i):
        if block.get_hash() == hash:     
            return i
        ans=list()
        for child in block.children:   
            ans.append(self.helper(child,hash,i+1))
        for i in ans:
            if i is not None:
                return i
        
    def distance(self,block,hash):
        i=self.helper(block,hash,0)
        return i
    
    def get_selfish_block(self,block,i):
        if i==0:
            return block
        else:
            for child in block.children:
                return self.get_selfish_block(child,i-1)
    
        
