from src import DAG
from src import Parser
import sys
import time

def process(file:str):
    with open(file) as f:
        data = [line for line in f.readlines()]
    return data

def main(name:str):

    if len(name)<1: 
        print("ERROR: no file in input.")
    else:
        file = "data/" + name

    if not file.endswith(".txt"): 
        print("ERROR: file are accepted in the form of text files only! Please check your input.")
        exit()

    #instantiate classes
    solver = DAG()
    parser = Parser()

    input = process(file)
    parsed_input = parser.parse(input)


if __name__ == "__main__":

    #start clock
    start = time.clock()

    #start procedure
    main(sys.argv[1])
    
    #end clock
    end = time.clock()
    print("Finished! Run in :", end-start)