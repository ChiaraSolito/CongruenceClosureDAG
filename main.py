from src import dag
from src import dag_builder
from src import smt_parser
import sys
import time
from pathlib import Path

def process(file:str):
    path = Path(file)
    return path.read_text()

def main(name:str):

    if len(name)<1: 
        print("ERROR: no file in input.")
    else:
        file = "data/" + name

    if (not file.endswith(".txt")) or (not file.endswith('.smt2')): 
        print("ERROR: file are accepted in the form of text files or smt2 format only! Please check your input.")
        exit()

    #instantiate classes
    
    if file.endswith('.smt2'):
        parser = smt_parser()
        solver = parser.parse(file)
    else:
        parser = dag_builder()
        input = process(file)
        solver = parser.parse_equations(input)


if __name__ == "__main__":

    #start clock
    start = time.clock()

    #start procedure
    main(sys.argv[1])
    
    #end clock
    end = time.clock()
    print("Finished! Run in :", end-start)