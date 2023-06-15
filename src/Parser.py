import re
from src import DAG

class Parser:

    def __init__(self, data, dag: DAG):
        self.atom_dict = {}
        self.priginal_data = data
        self.dag = dag
        self.diseq = []
        self.eq = []

    def parse_equations(self, data):

        for element in data:

            if "!=" in element:

                couple = re.split('!=', element)
                self.dag.add_node(couple[0])
                self.dag.add_node(couple[1])

                couple[0] = hash(couple[0].strip())
                couple[1] = hash(couple[1].strip())

                self.diseq.append(couple)

            elif "=" in element:
                couple = re.split('=', element)

                self.dag.add_node(couple[0])
                self.dag.add_node(couple[1])

                couple[0] = hash(couple[0].strip())
                couple[1] = hash(couple[1].strip())

                self.eq.append(couple)

            else:
                self.add_node(element)
                self.add_node("tt")
                couple[0] = hash(element.strip())
                couple[1] = hash("tt")

                self.eq.append(couple)

    def parse(self, data):
        return
