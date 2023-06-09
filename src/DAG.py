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
        m_ccpar = set()
        m_find = []
        m_find.append(id)
        self.g.add_node(id,fn=fn, args=args, m_find=m_find,m_ccpar=m_ccpar)
    
    def node(self, i:int):
        return self.g.nodes[i]
    
    def find(self, i:int):
        n = self.node(i)
        if n["m_find"] == i: 
            return i
        else:
            self.find(n["m_find"]) 
    
    def union(self, i1:int, i2:int):
        n1 = self.find(i1)
        n2 = self.find(i2)

        n1["find"] = n2["find"]
        n2["m_ccpar"].update(n1["m_ccpar"])
        n1["m_ccpar"].clear()
    
    def ccpar(self, i:int):
        return self.node(self.find(i))["m_ccpar"]
    
    def congruent(self, i1:int, i2:int):
        
        return 
    
    def merge(self, i1:int, i2:int):
        return 




