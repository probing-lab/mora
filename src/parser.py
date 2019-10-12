
from diofant import ( symbols, prod, Function, simplify, sympify, rsolve )
from utils import *

class InputParser:
    def __init__(self, input, input_format="file"):
        self.input_format = input_format
        self.variables = []
        self.parameters = []
        self.initial_values = {}
        self.goals = []
        self.updates = {}
        self.program_name = None
        self._parse_program(self._get_program(input))
        self._fill_in_inits()
        self._get_parameters()

    def _get_program(self, input):
        if self.input_format == "file":
            from pathlib import Path
            prog = Path("{}".format(input)).read_text()
            self.program_name = Path("{}".format(input)).name
        elif self.input_format == "string":
            import time
            prog = input
            self.program_name = "string_input_{}".format(time.strftime("%Y%m%d-%H%M%S"))
        else:
            raise Exception("Unknown input format: {}. Terminating.".format(self.input_format))
        return prog

    def __str__(self):
        return self.__repr__() ## " to do"

    def _parse_program(self, txt):
        initials, updates = map(str.strip, txt.split("while true:"))
        self._parse_update_assignments(updates)
        self._parse_initial_assignments(initials)

    def _parse_initial_assignments(self, txt):
        inits = map(str.strip, txt.split("\n"))
        for init in inits:
            self._parse_initial(init)

    def _parse_update_assignments(self, txt):
        updates = map(str.strip, txt.split("\n"))
        for update in updates:
            self._parse_update(update)

    def _parse_update(self, update_ln):
        var, update = map(str.strip, update_ln.split("="))
        var = symbols(var)
        self.variables.append(var)
        self.updates[var] = Update(var, update)


    def _parse_update_branch(self, txt):
        #doni in Update class
        pass
        return [("expr", "prob")]

    def _parse_initial(self, init_ln):
        var, val = map(str.strip, init_ln.split("="))
        var = symbols(var)
        #val = sympify(val)
        if var in self.variables:
            self.initial_values[var] = Update(var, val)

    def _parse_goal(self, txt):
        goal = map(simpify, map(str.strip, txt.split(" ")))

    def _fill_in_inits(self):
        # Variables with no initial value given we initialize
        # as parameters, e.g. x(0) as x0.
        for v in self.variables:
            if v not in self.initial_values:
                self.initial_values[v] = Update(v, "RV(unknown)")

    def _get_parameters(self):
        # Extract all variables from updates and ignore the program variables
        fvars = set()
        for var, update in self.updates.items():
            fvars = fvars.union(update.update_term(var, 1).free_symbols)
        return ' '.join(map(str, fvars.difference(self.variables)))



class OutputParser:
    def __init__(self, prog, invariants, time, output_format="tex"):
        program_name = prog.program_name
        goal = prog.goals
        if output_format == "tex" or output_format == "latex":
            from diofant import latex
            with open("out/tex_{}".format(program_name),"a+") as f:
                f.write("Moment based invariants for {}, with $[{}]$ as goal:\n".format(program_name, ", ".join([latex(g) for g in goal])))
                f.write("Computation took {}s.".format(time))
                for k in invariants:
                    if k:
                        f.write("\[E[{}] = {}\]\n".format(latex(k), latex(invariants[k])))
                f.write("\n\n")
        elif output_format == "txt":
            from diofant import latex
            with open("out/txt_{}".format(program_name),"a+") as f:
                f.write("Moment based invariants for {}, with [{}] as goal:\n".format(program_name, ", ".join([str(g) for g in goal])))
                f.write("Computation took {}s.".format(time))
                for k in invariants:
                    if k:
                        f.write("\nE[{}] = {}".format(k, invariants[k]))
                f.write("\n\n")
        else:
            print("Moment based invariants for {}, with [{}] as goal:\n".format(program_name, ", ".join([str(g) for g in goal])))
            print("Computation took {}s.".format(time))
            for k in invariants:
                if k:
                    print("E[{}] = {}".format(k, invariants[k]))
