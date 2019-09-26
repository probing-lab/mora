
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

        #updates = {
        #        f : Update(f, "", is_random_var=True, random_var=UniformVar(-1, 1)),
        #        x : Update(x, "x + f @ 1"),
        #        y : Update(y, "y - f @ 1"),
        #        p : Update(p, "x + y @ 1")
        #    }

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
        ###case rnd update
        #if '@' not in update:
        #    update += "1@1"
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

    def _update_free_vars(self):
        fvars = set()
        for var, update in self.updates.items():
            y = update.update_term(var, 1)
            print("    YYY ", y, type(y))
            x = y.free_symbols
            fvars = fvars.union(x)
        return fvars

    def _distributions_free_vars(self):
        pass

        ## todo:
        # get list of free_symbols (e.g. vars + arameters) using
        # exp.free_symbols whenever ext is compudet (updates and RV parameters)
        # use to find parameters (=free_symbols\variables)


prog = InputParser("""x = 0
y = 0
while true:
    u = uniform(0, a) @ 1/2
    x = x + u @ 1
    y = y + x - 2*u @ 1""")

print("initial ", prog.initial_values)
print("vars ", prog.variables)
print("upds ", prog.updates)
print("goals ", prog.goals)

######################
######################

x, y, s = symbols("x y s")
f, u1, u2 = symbols("f u1 u2")
d = symbols("d")

x0 = symbols('x(0)')

vars = [u1, u2, f, x, y, s]
rvars = vars[::-1]
# rank = {x:0, y:1}
initial = {f:0, x:x0, y:0, s:0}
#initial = {f:0, x:x0, y:UniformVar(0, 1), s:0} !!!not ok
parameters = [d]
goal = [s**2]
updates = {
        #f : Update(f, "", is_random_var=True, random_var=UniformVar(-1, 1)),
        u1 : Update(u1, "", is_random_var=True, random_var=UniformVar(1-d, 1+d)),
        u2 : Update(u2, "", is_random_var=True, random_var=UniformVar(2-2*d, 2+2*d)),
        f : Update(f, "1 @ 3/4; 0 @ 1/4"),
        x : Update(x, "x + f * u1 @ 1"),
        y : Update(y, "y + f * u2 @ 1"),
        s : Update(s, "s + x * y @ 1")

        # x: Update(x, "x + f @ 1"),
        # y: Update(x, "y @ 1/2; y + 2*x @ 1/2")
    }


class OutputParser:
    def __init__(self, invariants):
        pass
