from src.dag import DAG
from src.parser import Parser
from src.smt_parser import SmtParser
import time
import sys 

def process(file:str):
    with open(file) as f:
        return [line.rstrip('\n') for line in f.readlines()]

def main(name:str):
    #start clock
    start = time.perf_counter()

    if len(name)<1: 
        print("ERROR: no file in input.")
    else:
        file = "data/" + name

    if not file.endswith(".txt") and not file.endswith('.smt2'): 
        print("ERROR: file are accepted in the form of text files or smt2 format only! Please check your input.")
        exit()

    #instantiate classes
    
    if file.endswith('.smt2'):
        parser = SmtParser()
        solver = parser.parse(file)
    else:
        dag = DAG()
        parser = Parser(dag)
        input = process(file)
        parser.parse_formula(input)

        # merge of all node that are in equivalence relation
        satisfable = True
        for coppiaeq in dag.equalities:
            if satisfable:
                satisfable = dag.merge(dag.g.nodes[coppiaeq[0]], dag.g.nodes[coppiaeq[1]]) 
                #non funziona così perché i miei nodi non sono identificati da questo
                pass

        if satisfable:
            print('The formula is satisfiable! You can look at the graph generated.')
            #end clock
            end = time.perf_counter()
            print("Runned in :", end-start)
            dag.print_graph()
        else:
            print('The formula is unsatisfiable! We will now terminate the execution.')
            #end clock
            end = time.perf_counter()
            print("Runned in :", end-start)



if __name__ == "__main__":

    #start procedure
    if len(sys.argv)>1:
        main(sys.argv[1])    
    else:
        print('Please insert an input.')