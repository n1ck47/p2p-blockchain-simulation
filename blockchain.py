from block import GenesisBlock,Block

class Blockchain:
    def __init__(self):
        self.genesis=GenesisBlock()
        self.total=1
    
    def height(self,node):
        # print(node.get_hash(), len(node.children))
        # print(self.display_chain())
        if len(node.children) == 0:
            return (1, node)
        else:
            heights = [self.height(child) for child in node.children]
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, last_block)
    
    def findprevblock(self,node,prevhash):
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
        new_block = block.get_copy()
        prevhash=block.prev_hash
        prevblock=self.findprevblock(self.genesis,prevhash)
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


# blkchain=Blockchain()
# b1=Block('0'*256)
# b2=Block(b1.id)
# b3=Block(b1.id)
# b4=Block(b3.id)
# b5=Block(b4.id)
# blkchain.add_block(b1)
# blkchain.add_block(b2)
# blkchain.add_block(b3)
# blkchain.add_block(b4)
# print(b4.id)
# print(blkchain.getlastblock().id)
# print(blkchain.display_chain())
