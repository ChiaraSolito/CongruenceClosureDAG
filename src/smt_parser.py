from pysmt.smtlib.parser import SmtLibParser
import re

class SmtParser():
    def __init__(self):
        self.parser = SmtLibParser()

    def parse(self,filename):

        script = self.parser.get_script_fname(filename)
        f = script.get_strict_formula()

        result = [cmd for cmd in script.commands if ((cmd.name == "set-info") and (":status" in cmd.args))]

        assert len(result) <= 1
        assert script.count_command_occurrences("assert") >= 1
        assert script.contains_command("check-sat")

        formulas = f.serialize()
        formulas = formulas[1:] 
        formulas = formulas[:-1]

        final_formulas = []
        #formulas.remove
        if '&' in formulas:
            couple = re.split('&', formulas)

            for c in couple:
                c = c.strip(' ')
                
                if '! ' in c:
                    c = c.replace('=','!=')
                    c = c[3:]
                    c = c[:-1]
                c = c.strip('(')
                c = c.strip(')')
                final_formulas.append(c) 

        else:

            if '! ' in formulas:
                formulas = formulas.replace('=','!=')
                formulas = formulas[3:]
                formulas = formulas[:-1]
            c = c.strip('(')
            c = c.strip(')')
            final_formulas.append(c) 

        return final_formulas