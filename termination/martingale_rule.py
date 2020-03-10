"""
This module implements the general proof rule for AST
"""

from diofant import limit, symbols, oo, sympify, simplify
from termination.expression import get_branches_for_expression
from termination.invariance import is_invariant
from termination.rule import Rule, Result


class MartingaleRule(Rule):
    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        return lim == 0

    def run(self):
        pre_expressions = get_branches_for_expression(sympify(self.program.loop_guard), self.program)
        pre_expressions = [(simplify(e - sympify(self.program.loop_guard)), p) for e, p in pre_expressions]
        for e, p in pre_expressions:
            if is_invariant(e, self.program):
                # TODO check asymptotic behavior (not sound yet)
                return Result.AST
        return Result.UNKNOWN
