
from diofant import ( symbols, prod, Function, simplify, sympify, rsolve )
from utils import *
import ply.lex as lex

class InputParser:
    def __init__(self, program):
        self.variables = []
        self.parameters = []
        self.initial_values = {}
        self.goals = []
        self.updates = {}
        self._parse_program(program)
        self._fill_in_inits()
        self._get_parameters()

    def __str__(self):
        return self.__repr__() + " to do"##

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

    def _parse_initial(self, txt):
        var, val = map(str.strip, txt.split("="))
        var = symbols(var)
        val = sympify(val)
        if var in self.variables:
            self.initial_values[var] = val

    def _parse_goal(self, txt):
        goal = map(simpify, map(str.strip, txt.split(" ")))

    def _fill_in_inits(self):
        # Variables with no initial value given we initialize
        # as parameters, e.g. x(0) as x0.
        for v in self.variables:
            if v not in self.initial_values:
                self.initial_values[str(v)] = str(v)+"0"

    def _get_parameters(self):
        # Extract all variables from updates and ignore the program variables
        fvars = set()
        for var, update in self.updates.items():
            fvars = fvars.union(update.update_term(var, 1).free_symbols)
        return ' '.join(map(str, fvars.difference(self.variables)))



class OutputParser:
    def __init__(self, invariants):
        pass
