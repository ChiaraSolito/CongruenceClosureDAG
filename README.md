# Congruence Closure DAG

This project aims to implement the congruence closure algorithm with DAG to satisfy a set of equalities and disequalities in the quantifier-free fragment of the theory of equality.

## Requirments

To run the algorithm it is required to have installed [Python3](https://www.python.org/downloads/)\
Better if version 3.11.

## How to run the first time

- Insert file to test in folder 'data'
- Run ```./run.sh```
- Insert the name of the file (with extension) in the command line, when asked.

### How to run following times

You will only need to activate the environment, and then run the main script.

```(bash)
source ./venv/bin/activate
python3 main.py
```

## Type of accepted input

### Text files

Files with '.txt' extension are accepted if they are presented in AND with each other.\
Each equality and disequality to be in consider in the algorithm must be put on different lines.

Example of structure of a 'input.txt' file:

```(txt)
    f(a,b) = a
    f(a,b) != a
```

### Important for text files

- All equalities and inequalities in AND.
- No brackets around the outermost symbols.

This will be interpreted as 'f(a,b) = a & f(a,b) != a'

### SMT files

Smt2 format is accepted only when formulas are in AND with eachother.\
As for the text files, the formula is read as different equalities and disequalities in AND.

Example of structure of a 'input.smt2' file:

```(smt2)
    (set-info :smt-lib-version 2.6)
    (set-logic QF_UF)
    (set-info :source |
    Source: The calcolus of computation (Bradley-Manna) 
    Translator: Andrea Mangrella. |)
    (set-info :category "crafted")
    (set-info :status unsat)
    (declare-sort S1 0)
    (declare-fun a () S1)
    (declare-fun b () S1)
    (declare-fun f (S1 S1) S1)
    (assert (let ((t1 (f a b)) (t2 (f t1 b ))) (and (= t1 a) (not (= t2 a) ))) )
    (check-sat)
    (exit)
```

This will be interpreted as 'f(a, b) = a & f(f(a, b), b) != a'. This precise example can be found in the data folder under the name of 'input1.smt2'.
