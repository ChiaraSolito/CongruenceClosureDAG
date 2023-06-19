from pysmt.smtlib.parser import SmtLibParser
from pysmt.rewritings import CNFizer 
cnf_parser = CNFizer()

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

        atoms = list(map(lambda x: x.strip(),separated_formulas))

        real_atoms,real_formulas = [],[]
        for atom in atoms:
            if atom.find("=") != -1:
                equality = atom[1:-1].split("=")
                real_atoms.append(equality[0].strip())
                real_atoms.append(equality[1].strip())
            else:
                real_atoms.append(atom)

        # Separate all Ands 
        if formulas.find("&") != -1:
            separated_formulas = formulas[1:-1].split("&")
            real_formulas.extend(list(map(lambda x: x.strip(),separated_formulas)))

        # Remove all non-equality formulas
        real_formulas = [x for x in real_formulas if x.find("=")!=-1 ]

        return real_formulas,set(real_atoms),ground_truth.upper()