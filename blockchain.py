from block import GenesisBlock,Block
class Blockchain:
    def __init__(self):
        self.genesis=GenesisBlock()
        self.total=1
    
    def height(self,node):
        if not node.children:
            return (1, node)
        else:
            heights = [self.height(child) for child in node.children]
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, last_block)
    
    def getlastblock(self):
        finalblock=self.height(self.genesis)[1]
        return finalblock
    
    def add_block(self,block):
        lastblock=self.getlastblock()
        lastblock.children.append(block)
        return
    def allnodesinchain(self,node):
        if not node.children:
            return (1, [node])
        else:
            heights = [self.allnodesinchain(child) for child in node.children]
            max_height, last_block = max(heights, key=lambda x: x[0])
            return (1 + max_height, [node] + last_block)
    def display_chain(self):
        return self.allnodesinchain(self.genesis)[1]


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