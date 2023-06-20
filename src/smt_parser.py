from pysmt.smtlib.parser import SmtLibParser
import re

class SmtParser():
    def __init__(self):
        self.parser = SmtLibParser()

    def parse(self,filename):

        script = self.parser.get_script_fname(filename)
        f = script.get_strict_formula()

        result = [cmd for cmd in script.commands if ((cmd.name == "set-info") and (":status" in cmd.args))]
        ground_truth = result[0].args[1]

        assert len(result) <= 1
        assert script.count_command_occurrences("assert") >= 1
        assert script.contains_command("check-sat")

        formulas = f.serialize()
        formulas = formulas[1:] 
        formulas = formulas[:-1]
        print(formulas)

        if '(! (' in formulas:
            formulas = formulas.replace('(! ','')
            formulas = formulas[:-1] 

        #formulas.remove
        if '&' in formulas:
            couple = re.split('&', formulas)
            couple[0] = couple[0][1:]
            couple[0] = couple[0][:-2]
            couple[1] = couple[1][2:]
            couple[1] = couple[1][:-1]

        return couple