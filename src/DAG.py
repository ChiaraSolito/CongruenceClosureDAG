import networkx as nx 
import itertools 
from uuid import uuid4

class DAG: 

    def __init__(self): 
        self.g = nx.DiGraph()
        self.equalities = []
        self.inequalities = []

    def add_node(self, fn, args:list):
        id = uuid4()
        m_ccpar = set()
        m_find = []
        m_find.append(id)
        self.g.add_node(id,fn=fn, args=args, m_find=m_find,m_ccpar=m_ccpar)
        return id 
    
    def add_edge(self,node1,node2):
        return self.g.add_edge(node1, node2)
    
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

        n1["m_find"] = n2["m_find"]
        n2["m_ccpar"].update(n1["m_ccpar"])
        n1["m_ccpar"].clear()
    
    def ccpar(self, i:int):
        return self.node(self.find(i))["m_ccpar"]
    
    def congruent(self, i1:int, i2:int):
        ris = True
        n1 = self.node(i1)
        n2 = self.node(i2)
        if n1["fn"]== n2["fn"] and len(n1["args"]) == len(n2["args"]):
            for a1 in n1["args"]:
                if ris:
                    ris = False
                    for a2 in n2["args"]:
                        if self.find(a1) == self.find(a2):
                            ris = True
        else:
            return False
        return ris
    
    def merge(self, i1:int, i2:int):
        if self.find(i1) != self.find(i2):
            Pi1 = self.ccpar(i1)
            Pi2 = self.ccpar(i2)
            union = self.union(i1,i2)

            for t1 in Pi1:
                for t2 in Pi2:
                    if self.find(t1) != self.find(t2) or self.congruent(t1,t2):
                        self.merge(t1,t2)
        return 




