import networkx as nx 
import itertools 

class DAG: 

    newid = itertools.count().next

    def __init__(self): 
        self.g = nx.DiGraph()
        self.equalities = []
        self.inequalities = []

    def add_node(self, fn, args:list):
        id = self.newid()
        mutable_ccpar = set()
        mutable_find = []
        mutable_find.append(id)
        self.g.add_node(id,fn=fn, args=args, mutable_find=mutable_find,mutable_ccpar=mutable_ccpar)
    
    def node(self, i:int):
        return self.g.nodes[i]
    
    def find(self, i:int):
        n = self.node(i)
        if n["mutable_find"] == i: 
            return i
        else:
            self.find(n["mutable_find"]) 
    
    def union(self, i1:int, i2:int):
        return 
    
    def ccpar(i:int):
        return
    
    def congruent(self, i1:int, i2:int):
        return 
    
    def merge(self, i1:int, i2:int):
        return 




