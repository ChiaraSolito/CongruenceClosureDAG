import networkx as nx 
from uuid import uuid4, UUID
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from itertools import combinations

class DAG: 

    def __init__(self): 
        self.g = nx.DiGraph()
        self.equalities = []
        self.inequalities = []

    def add_node(self, fn, args:list):
        id = uuid4()
        self.g.add_node(id,fn=fn, args=args, m_find=id,m_ccpar=set())
        return id 
        
    def add_edge(self, node1:UUID, node2:UUID):
        self.node(node2)["m_ccpar"].add(node1)
        self.node(node1)["args"].append(node2)
        return self.g.add_edge(node1, node2)
    
    def node(self, i:UUID):
        return self.g.nodes[i]
    
    def find(self, i:UUID):
        n = self.node(i)
        if n["m_find"] == i: 
            return i
        else:
            self.find(n["m_find"]) 
    
    def union(self, i1:UUID, i2:UUID):
        n1 = self.node(i1)
        n2 = self.node(i2)

        n1["m_find"] = n2["m_find"]
        n2["m_ccpar"].update(n1["m_ccpar"])
        n1["m_ccpar"].clear()

        return n1["m_ccpar"],n2["m_ccpar"]
    
    def ccpar(self, i:UUID):
        return self.node(i)["m_ccpar"]
    
    def congruent(self, i1:UUID, i2:UUID):
        ris = True
        n1 = self.node(i1)
        n2 = self.node(i2)
        if n1["fn"] == n2["fn"] and len(n1["args"]) == len(n2["args"]):
            for a1 in n1["args"]:
                if ris:
                    ris = False
                    for a2 in n2["args"]:
                        if self.find(a1) == self.find(a2):
                            ris = True
        else:
            return False
        return ris
    
    def merge(self, i1:UUID, i2:UUID):
        f1 = self.find(i1)
        f2 = self.find(i2)

        if f1 != f2:
            Pi1 = self.ccpar(i1)
            Pi2 = self.ccpar(i2)
            self.union(i1,i2)

            for t1 in Pi1:
                for t2 in Pi2:

                    print(t1)
                    print(t2)

                    if self.find(t1) != self.find(t2) or self.congruent(t1,t2):
                        self.merge(t1,t2)
    
    def simplify(self,eq,diseq):

        fns = [self.g.nodes[node]['fn'] for node in self.g.nodes]

        #first simplify leaves
        for fn in fns:
            leaves = [node for node in self.g.nodes if self.g.out_degree(node) == 0 and self.g.nodes[node]["fn"] == fn]

            if len(leaves)>1:
                newid = self.add_node(fn,[])

                predecessors = set()
                for node in leaves:
                    predecessors.update(self.g.predecessors(node))

                    eq = [[newid,item[1]] if item[0] == node else [item[0],item[1]] for item in eq]
                    eq = [[item[0],newid] if item[1] == node else [item[0],item[1]] for item in eq]
                    diseq = [[newid,item[1]] if item[0] == node else [item[0],item[1]] for item in diseq]
                    diseq = [[item[0],newid] if item[1] == node else [item[0],item[1]] for item in diseq]

                    self.g.remove_node(node)

                for predecessor in predecessors:
                    self.add_edge(predecessor, newid)

        #then simplify functions
        for fn in fns:
            non_leaves = [node for node in self.g.nodes if self.g.out_degree(node)>0 and self.g.nodes[node]["fn"] == fn]

            if len(non_leaves)>1:
                graph_copy = self.g.copy()

                #for each couple of nodes with the same fn
                for (u,v) in combinations(non_leaves,2):
                    #if they have the same list of successors we unify them
                    if list(graph_copy.successors(u)) == list(graph_copy.successors(v)):

                        newid = self.add_node(fn,[])

                        predecessors = set()

                        predecessors.update(graph_copy.predecessors(u))
                        predecessors.update(graph_copy.predecessors(v))

                        for predecessor in predecessors:
                            self.add_edge(predecessor, newid)
                        for successor in graph_copy.successors(u):
                            self.add_edge(newid,successor)
                        
                        #remove the node and substitute his id in the list of equalities

                        if self.g.has_node(u):
                            
                            eq = [[newid,item[1]] if item[0] == u else [item[0],item[1]] for item in eq]
                            eq = [[item[0],newid] if item[1] == u else [item[0],item[1]] for item in eq]

                            diseq = [[newid,item[1]] if item[0] == u else [item[0],item[1]] for item in diseq]
                            diseq = [[item[0],newid] if item[1] == u else [item[0],item[1]] for item in diseq]

                            self.g.remove_node(u)

                        #remove the node and substitute his id in the list of equalities
                        if self.g.has_node(v):

                            eq = [[newid,item[1]] if item[0] == v else [item[0],item[1]] for item in eq]
                            eq = [[item[0],newid] if item[1] == v else [item[0],item[1]] for item in eq]

                            diseq = [[newid,item[1]] if item[0] == v else [item[0],item[1]] for item in diseq]
                            diseq = [[item[0],newid] if item[1] == v else [item[0],item[1]] for item in diseq]

                            self.g.remove_node(v)

        return eq, diseq

    def print_graph(self):
        labels = nx.get_node_attributes(self.g, 'fn') 
        pos = graphviz_layout(self.g, prog="dot")
        nx.draw(self.g, pos, labels=labels, font_weight='bold')
        plt.show() 
        





