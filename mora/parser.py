
from diofant import ( symbols, prod, Function, simplify, sympify, rsolve )
from mora.utils import *

class InputParser:
    def __init__(self, input, input_format="file"):
        self.input_format = input_format
        self.variables = []
        self.parameters = []
        self.initial_values = {}
        self.goals = []
        self.updates = {}
        self.program_name = None
        self.ok = True
        self._parse_program(self._get_program(input))
        self._fill_in_inits()
        self._get_parameters()


    def _get_program(self, input):
        if self.input_format == "file":
            from pathlib import Path
            prog = Path("{}".format(input)).read_text()
            self.program_name = Path("{}".format(input)).name
        elif self.input_format == "string":
            prog = input
            self.program_name = "string_input"
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
        non_vars = set()
        for update in updates:
            non_vars = self._parse_update(update, non_vars)

    def _parse_update(self, update_ln, non_vars):
        var, update = map(str.strip, update_ln.split("="))
        var = symbols(var)
        if var in non_vars:
            self.ok = False
            print("Program not Prob-solvable. Terminating.")
        self.variables.append(var)
        self.updates[var] = Update(var, update)
        self.ok &= self.updates[var].ok
        return non_vars.union(self.updates[var].update_term(var, 1).free_symbols).difference(self.variables)


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
        # Extract all (free) variables from updates and ignore the program variables
        fvars = set()
        for var, update in self.updates.items():
            fvars = fvars.union(update.update_term(var, 1).free_symbols)
        return ' '.join(map(str, fvars.difference(self.variables)))



class OutputParser:
    def __init__(self, prog, invariants, computation_time, output_format=" "):
        program_name = prog.program_name
        goal = prog.goals
        from datetime import datetime
        from time import strftime
        timestamp = datetime.now().strftime('%y%m%d-%H%M%S%f')[:-4]
        if output_format == "tex" or output_format == "latex":
            from diofant import latex
            with open(f"out/{output_format}_{program_name}_{timestamp}","a+") as f:
                f.write("Moment based invariants for program {}, with invariants over $[{}]$.\n".format(program_name, ", ".join([latex(g) for g in goal])))
                for k in invariants:
                    if k:
                        f.write("\[E[{}] = {}\]\n".format(latex(k), latex(invariants[k])))
                f.write("\nComputation time {}s.".format(computation_time))
                f.write("\n\n")
        elif output_format == "text" or output_format == "eval" or output_format == "exp":
            with open(f"out/{output_format}_{program_name}_{timestamp}","a+") as f:
                f.write("Moment based invariants for program {}, with invariants over [{}]:\n".format(program_name, ", ".join([str(g) for g in goal])))
                for k in invariants:
                    if k:
                        f.write(f"\nE[{k}] = {invariants[k]}")
                f.write(f"\n\nComputation time {computation_time}s.")
                f.write("\n\n")
        #else:
        print(f"\nMoment based invariants for program {program_name}, with invariants over [{', '.join([str(g) for g in goal])}]:")
        for k in invariants:
            if k:
                print(" E[{}] = {}".format(k, invariants[k]))
        print("Computation time {}s.".format(computation_time))
