from src.dag import DAG
from src.parser import Parser
from src.smt_parser import SmtParser
import time

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
    dag = DAG()
    parser = Parser(dag)

    if file.endswith('.smt2'):
        smt = SmtParser()
        input = smt.parse(file)
        form = ' & '.join(input)
        print(f'Final form of the input is: {form}')
    else:
        input = process(file)
        form = ' & '.join(input)
        print(f'Final form of the input is: {form}')
    
    dag.g, eq, diseq = parser.parse_formula(input)

    # merge of all node that are in equivalence relation
    satisfiable = True

    for couple in eq:
        dag.merge(couple[0], couple[1]) 
    
    for couple in diseq:
        if dag.find(couple[0]) == dag.find(couple[1]):
            satisfiable = False

    if satisfiable:
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
        dag.print_graph()



if __name__ == "__main__":

    #start procedure
    
    file = input('Please insert an input or h to get help: ')
    if file == 'h':
        print()
    else:
        main(file)