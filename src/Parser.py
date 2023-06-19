import re
from DAG import DAG
from pyparsing import nestedExpr
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

class Parser:

    def __init__(self, dag: DAG):
        self.atom_dict = {}
        #self.original_data = data
        self.dag = dag
        self.diseq = []
        self.eq = []

    def parse_equations(self, data):

        if "!=" in data:

            couple = re.split('!=', data)

            self.parse_expression("(" + couple[0] + ")")
            self.parse_expression("(" + couple[1] + ")")

            self.diseq.append(couple)

        elif "=" in data:
            couple = re.split('=', data)

            self.parse_expression("(" + couple[0] + ")")
            self.parse_expression("(" + couple[1] + ")")

            self.eq.append(couple)

        else:
            self.parse_expression(data)

    def parse(self,list_elements:list):
        nodes = []

        for element in list_elements:
            print(f"element: {element}")
            if isinstance(element,str):

                nodes.append(self.dag.add_node(element,[]))

            else:
                parent = nodes[-1]
                print(f"parent: {parent}")

                nodes2 = self.parse(element)

                for node in nodes2:
                    self.dag.add_edge(parent,node)

        return nodes

    def parse_expression(self,expression:str):
        expr = nestedExpr()  
        expression = expression.replace("," , " ")
        print(expression)
        list_nested = expr.parseString(expression).as_list()
        self.parse(list_nested[0])

    def print_graph(self):
        labels = nx.get_node_attributes(self.dag.g, 'fn') 
        nx.draw(self.dag.g, labels=labels, font_weight='bold')
        plt.show() 

# Test dell'esempio
expression = "f(f(a,b),b)=f(a,b),g(a)"
dag = DAG()
parser = Parser(dag)
graph = parser.parse_equations(expression)
parser.print_graph()