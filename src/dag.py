import networkx as nx 
from uuid import uuid4, UUID
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from itertools import combinations
import copy

class DAG: 

    def __init__(self): 
        self.g = nx.DiGraph()
        self.equalities = []
        self.inequalities = []

    def add_node(self, fn, args:list):
        id = uuid4()
        self.g.add_node(id, fn=fn, args=args, m_find=id, m_ccpar=set())
        return id 
        
    def add_edge(self, node1:UUID, node2:UUID):
        self.node(node2)["m_ccpar"].add(node1)
        self.node(node1)["args"].append(node2)
        return self.g.add_edge(node1, node2)

    def remove_edge(self, node1:UUID, node2:UUID):
        if node1 in self.node(node2)["m_ccpar"]:
            self.node(node2)["m_ccpar"].remove(node1)
        if node2 in self.node(node1)["args"]:
            self.node(node1)["args"].remove(node2)
    
    def node(self, i:UUID):
        return self.g.nodes[i]
    
    def find(self, i:UUID):
        n = self.node(i)

        if n["m_find"] == i: 
            return i
        else:
            return self.find(n["m_find"]) 
    
    def union(self, i1:UUID, i2:UUID):
        n1 = self.node(self.find(i1))
        n2 = self.node(self.find(i2))

        #il ccpar maggiore quello che prevale

        n1["m_find"] = n2["m_find"]

        if len(n1["m_ccpar"]) > len(n2["m_ccpar"]):
            n1["m_ccpar"] = n1["m_ccpar"].union(n2["m_ccpar"])
            n2["m_ccpar"] = set()
        else:
            n2["m_ccpar"] = n2["m_ccpar"].union(n1["m_ccpar"])
            n1["m_ccpar"] = set()

        return n1["m_ccpar"],n2["m_ccpar"]
    
    def ccpar(self, i:UUID):
        return self.node(self.find(i))["m_ccpar"]
    
    def congruent(self, i1:UUID, i2:UUID):
            
        n1 = self.node(i1)
        n2 = self.node(i2)
        if not (n1["fn"] == n2["fn"]): 
            return False
        elif not((len(n1["args"]) == len(n2["args"]))): 
            return False
        
        for i in range(len(n1["args"])):
            val1 = self.find(n1["args"][i]) 
            val2 = self.find(n2["args"][i]) 
            if val1 != val2: 
                return False
        return True
    
    def merge(self, i1:UUID, i2:UUID):
        f1 = self.find(i1)
        f2 = self.find(i2)

        if f1 != f2:
            Pi1 = copy.copy(self.ccpar(i1))
            Pi2 = copy.copy(self.ccpar(i2))

            self.union(i1,i2)
            
            for t1 in Pi1:
                for t2 in Pi2:

                    if self.find(t1) != self.find(t2) and self.congruent(t1,t2):
                        self.merge(t1,t2)
    
    def simplify(self,eq,diseq):

        fns = {self.g.nodes[node]['fn'] for node in self.g.nodes}

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

                    for predecessor in self.g.predecessors(node):
                        self.remove_edge(predecessor,node)
                    self.g.remove_node(node)

                for predecessor in predecessors:
                    self.add_edge(predecessor, newid)

        #then simplify functions
        for fn in fns:
            non_leaves = [node for node in self.g.nodes if self.g.out_degree(node)>0 and self.g.nodes[node]["fn"] == fn]
            comb = list(combinations(non_leaves,2))
            if len(non_leaves)>1:

                #for each couple of nodes with the same fn
                #for (u,v) in comb:
                
                i = 0
                while i < len(comb):

                    u,v = comb[i]
                    if u in self.g.nodes() and v in self.g.nodes():
                        #if they have the same list of successors we unify them
                        if list(self.g.successors(u)) == list(self.g.successors(v)):

                            newid = self.add_node(fn,[])

                            predecessors = set()

                            predecessors.update(self.g.predecessors(u))
                            predecessors.update(self.g.predecessors(v))

                            for predecessor in predecessors:
                                self.add_edge(predecessor, newid)
                            for successor in self.g.successors(u):
                                self.add_edge(newid,successor)
                            
                            #remove the node and substitute his id in the list of equalities

                            if self.g.has_node(u):
                                
                                eq = [[newid,item[1]] if item[0] == u else [item[0],item[1]] for item in eq]
                                eq = [[item[0],newid] if item[1] == u else [item[0],item[1]] for item in eq]

                                diseq = [[newid,item[1]] if item[0] == u else [item[0],item[1]] for item in diseq]
                                diseq = [[item[0],newid] if item[1] == u else [item[0],item[1]] for item in diseq]

                                #remove predecessor and successors
                                for predecessor in self.g.predecessors(u):
                                    self.remove_edge(predecessor,u)
                                for successor in self.g.successors(u):
                                    self.remove_edge(u,successor)
                                self.g.remove_node(u)

                            #remove the node and substitute his id in the list of equalities
                            if self.g.has_node(v):

                                eq = [[newid,item[1]] if item[0] == v else [item[0],item[1]] for item in eq]
                                eq = [[item[0],newid] if item[1] == v else [item[0],item[1]] for item in eq]

                                diseq = [[newid,item[1]] if item[0] == v else [item[0],item[1]] for item in diseq]
                                diseq = [[item[0],newid] if item[1] == v else [item[0],item[1]] for item in diseq]

                                #remove edges before removing nodes
                                for predecessor in self.g.predecessors(v):
                                    self.remove_edge(predecessor,v)
                                for successor in self.g.successors(v):
                                    self.remove_edge(v,successor)
                                self.g.remove_node(v)

                            #update non_leaves and comb
                            non_leaves = [node for node in self.g.nodes if self.g.out_degree(node)>0 and self.g.nodes[node]["fn"] == fn]    
                            comb = list(combinations(non_leaves,2))
                            i = -1
                    i += 1   

        return self.g, eq, diseq

    def print_graph(self):
        labels = nx.get_node_attributes(self.g, 'fn') 
        pos = graphviz_layout(self.g, prog="dot")
        nx.draw(self.g, pos, labels=labels, font_weight='bold')
        plt.show() 

    def print_final_graph(self):
        final_graph = self.g.copy()

        edges_find = []
        #edges_ccpar = []
        for u in final_graph.nodes():
            node = final_graph.nodes[u]

            #add find edges
            if str(node["m_find"]) != str(u):
                edges_find.append((u,node["m_find"]))
            #add ccpar edges

            # if len(node["m_ccpar"])>0:
            #     for v in node["m_ccpar"]:
            #         #only if it's not its direct parent
            #         if u not in final_graph.nodes[v]["args"]:
            #             edges_ccpar.append((v,u))

        labels = nx.get_node_attributes(final_graph, 'fn') 
        pos = graphviz_layout(final_graph, prog="dot")

        nx.draw_networkx_edges(final_graph, pos=pos,edgelist=edges_find, style = 'dashed',connectionstyle='arc3 ,rad=0.3')
        #nx.draw_networkx_edges(final_graph, pos=pos,edgelist=edges_ccpar, style = 'dashdot',connectionstyle='arc3 ,rad=0.3')
        nx.draw(final_graph, pos, labels=labels, font_weight='bold')
        plt.show() 





