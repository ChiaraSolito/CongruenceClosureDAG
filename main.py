from src.dag import DAG
from src.parser import Parser
from src.smt_parser import SmtParser
import time

def process(file:str):
    with open(file) as f:
        return [line.rstrip('\n') for line in f.readlines()]

def main(name:str):

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
        print(f'Final form of the input is: {form}.\n You can look at the generated graph. Close the image to continue.')
        print()
    else:
        input = process(file)
        form = ' & '.join(input)
        print(f'Final form of the input is: {form}.\n You can look at the generated graph. Close the image to continue.')
        print()

    dag.g, eq, diseq = parser.parse_formula(input)
    dag.print_graph()

    #start clock
    start = time.perf_counter()

    # merge of all node that are in equivalence relation
    satisfiable = True

    for couple in eq:
        dag.merge(couple[0], couple[1]) 
    
    for couple in diseq:
        if dag.find(couple[0]) == dag.find(couple[1]):
            satisfiable = False

    if satisfiable:
        print('The formula is satisfiable!')
        #end clock
        end = time.perf_counter()
        print("Time to compute satisfiability: ", end-start)
        print()
        print("Final graph generated from the algorithm. Close the image to end the script execution.")
        dag.print_final_graph()
    else:
        print('The formula is unsatisfiable!')
        print()
        #end clock
        end = time.perf_counter()
        print("Time to compute unsatisfiability: ", end-start)
        print("Final graph generated from the algorithm. Close the image to end the script execution.")
        dag.print_final_graph()



if __name__ == "__main__":

    #start procedure
    
    file = input('Please insert an input or h to get help: ')
    if file == 'h':
        print()
    else:
        main(file)