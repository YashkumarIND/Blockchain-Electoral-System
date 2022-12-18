import sys
print(sys.setrecursionlimit(200000))

import hashlib


import datetime

current_time = datetime.datetime.now()


class Block:
    def __init__(self,merkle_root):
        self.block_number = None
        self.data = None
        self.prev_hash = None
        self.curr_hash = None
        self.merkle_root=merkle_root
        self.nonce=None #here different use for solving repeating hash problem
        self.timestamp=None

    def __str__(self):
        return f"Block: \n{self.block_number}\n{self.data}\n{self.prev_hash}\n{self.curr_hash}\n{self.merkle_root}\n{self.nonce}\\n{self.timestamp}"


prev_hash='91b4d142823f7d20c5f08df69122de43f35f057a988d9619f6d3138485c9a203'
node_hash = hashlib.sha256('Voting data'.encode('utf-8')).hexdigest()
curr_hash = hashlib.sha256((node_hash + prev_hash).encode('utf-8')).hexdigest()

class Blockchain:
    curr_hash = hashlib.sha256((node_hash + prev_hash).encode('utf-8')).hexdigest()
    blockchain = []
    merkle_hashes = []
    block_number = 1
    merkle_root=curr_hash
    node = Block(node_hash)
    node.data={'Voting Data':'1'}
    node.block_number=1
    node.nonce=str(113)
    node.prev_hash=prev_hash
    node.curr_hash=curr_hash
    node.timestamp = current_time
    blockchain.append(node)
    merkle_hashes.append([{'root_merkle': node_hash}, {'level_2': 0}, {'level_3': 0}])


    def __init__(self,node_hash):
        self.node_hash=node_hash


    def merkle_tree(self,list_transact):
        keys = list(list_transact.keys())
        values=list(list_transact.values())
        t1=keys[0]+values[0]
        t2=keys[1]+values[1]
        t3=keys[2]+values[2]
        t4=keys[3]+values[3]
        t5=keys[4]+values[4]
        t6=keys[5]+values[5]
        t=[t1,t2,t3,t4,t5,t6]
        node1=hashlib.sha256((t[0]+t[1]).encode('utf-8')).hexdigest()
        node2=hashlib.sha256((t[2]+t[3]).encode('utf-8')).hexdigest()
        node3=hashlib.sha256((t[4]+t[5]).encode('utf-8')).hexdigest()
        level_2=[node1,node2,node3]
        node4=hashlib.sha256((node1+node2).encode('utf-8')).hexdigest()
        level_3=[node4,node3]
        merkle_root=hashlib.sha256((node4+node3).encode('utf-8')).hexdigest()
        self.merkle_hashes.append([{'root_merkle':merkle_root},{'level_2':level_2},{'level_3':level_3}])

        print(self.merkle_hashes)

        return merkle_root


    def get_prev_block(self):
        return self.blockchain[-1]


    def proof_of_work(self,Nonce,prev_hash):
        target_hash=hashlib.sha256((prev_hash+Nonce).encode('utf-8')).hexdigest()
        if target_hash[:1]!='0':
            return self.proof_of_work(str(int(Nonce)+1),prev_hash)
        return target_hash


    def is_valid(self,block):
        prev_block=self.get_prev_block()
        proof_of_work=self.proof_of_work(block.nonce,prev_block.curr_hash)
        if (block.prev_hash==prev_block.curr_hash) and (proof_of_work==block.curr_hash):
            return True
        return False


    def insert_block(self, data):#Mine a new Block with six transactions from mempool
        merkle_root=self.merkle_tree(data)
        newNode=Block(merkle_root)
        newNode.data=data
        prev_block=self.get_prev_block()
        nonce=str(int(prev_block.nonce)+1)
        newNode.nonce=nonce
        newNode.prev_hash=prev_block.curr_hash
        proof_of_work=self.proof_of_work(nonce,prev_block.curr_hash)
        newNode.curr_hash=proof_of_work
        newNode.block_number=self.block_number+1
        newNode.timestamp=current_time
        is_valid=self.is_valid(newNode)
        print(is_valid)
        if is_valid:
            self.blockchain.append(newNode)
            self.node_hash=newNode.curr_hash
        else:
            return "Block is invalid!"


        return "Blocked Mined Successfully!"






blockchain=Blockchain(curr_hash)
mem = {'994968317349': 'SankiSarkar', '292916015840': 'SankiSarkar', '259326718916': 'ShreyuSarkar', '719889320346': 'TinguSarkar', '912779882179': 'SidEkNamuna', '994968317347': 'SankiSarkar'}
print(blockchain.insert_block(mem))
print(blockchain.merkle_tree(mem))
