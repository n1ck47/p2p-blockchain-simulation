from block import GenesisBlock,Block
import queue

class Blockchain:
    def __init__(self):
        self.genesis=GenesisBlock()
        self.total=1
    
    def height(self,node):
        # print(node.get_hash(), len(node.children))
        # print(self.display_chain())
        if node is None:
            return (0, None)
        if len(node.children) == 0:
            return (1, node)
        else:
            heights = [self.height(child) for child in node.children]
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, last_block)
    
    def findprevblock(self,node,prevhash):
        if node is None:
            return None
        if node.get_hash()==prevhash:
            return node
        else:
            for child in node.children:
                result=self.findprevblock(child,prevhash)
                if result:
                    return result
            return None
        
    
    def getlastblock(self):
        finalblock=self.height(self.genesis)[1]
        return finalblock
    
    def add_block(self,block):
        if block is None:
            return 
        new_block = block.get_copy()
        prevhash=block.prev_hash
        prevblock=self.findprevblock(self.genesis,prevhash)
        if prevblock is None:
            return
        prevblock.children.append(new_block)

    def block_exist(self,block, current_block):
        if current_block is None:
            current_block = self.genesis
        # print('exist', len(current_block.children), block.get_hash() == current_block.get_hash(),  block.get_hash(), current_block.get_hash())
        if block.get_hash() == current_block.get_hash():
            return True
        for child in current_block.children:
            if(self.block_exist(block, child)):
                return True
        return False

    def allnodesinchain(self,node):
        # print(node.get_hash(), len(node.children), 'dis')
        if not node.children:
            return (1, [node])
        else:
            heights = [self.allnodesinchain(child) for child in node.children]
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, [node] + last_block)
        
    def display_chain(self):
        return [node.get_hash() for node in self.allnodesinchain(self.genesis)[1]]
    
    def get_blockchain_tree(self):

        adjancency_list = {}
        block = self.genesis
        blocks_queue = queue.Queue()
        blocks_queue.put(self.genesis)

        while(not blocks_queue.empty()):
            block = blocks_queue.get()
            adjancency_list[str(block.id)] = [ str(i.id) for i in block.children]

            for bl in block.children:
                blocks_queue.put(bl)
        
        return adjancency_list