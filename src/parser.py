import re
from src.dag import DAG
from pyparsing import nestedExpr

class Parser:

    def __init__(self, dag: DAG):
        self.dag = dag
        self.diseq = []
        self.eq = []

    def parse_formula(self, data):
        #parse each line of the formula as if in AND
        for line in data:
            self.parse_equations(line)

        return self.dag.simplify(self.eq, self.diseq)

    def parse_equations(self, data):

        if "!=" in data:

            couple = re.split('!=', data)

            root1 = self.parse_expression("(" + couple[0] + ")")[0]
            root2 = self.parse_expression("(" + couple[1] + ")")[0]

            self.diseq.append([root1,root2])

        elif "=" in data:
            couple = re.split('=', data)

            root1 = self.parse_expression("(" + couple[0] + ")")[0]
            root2 = self.parse_expression("(" + couple[1] + ")")[0]

            self.eq.append([root1,root2])

        else:
            self.parse_expression("(" + data + ")")

    def parse(self,list_elements:list):
        nodes = []

        for element in list_elements:
            #print(f"element: {element}")
            if isinstance(element,str):

                nodes.append(self.dag.add_node(element,[]))

            else:
                parent = nodes[-1]
                #print(f"parent: {parent}")

                nodes2 = self.parse(element)

                for node in nodes2:
                    self.dag.add_edge(parent,node)

        return nodes

    def parse_expression(self,expression:str):
        expr = nestedExpr()  
        expression = expression.replace("," , " ")
        #print(expression)
        list_nested = expr.parseString(expression).as_list()
        return self.parse(list_nested[0])