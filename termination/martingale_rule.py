"""
This module implements the general proof rule for AST
"""

from diofant import limit, symbols, oo, sympify, simplify

from termination import bound_store
from termination.asymptotics import is_dominating_or_same, Direction
from termination.expression import get_branches_for_expression
from termination.invariance import is_invariant
from termination.rule import Rule, Result


class MartingaleRule(Rule):
    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        return lim == 0

    def run(self):
        # Martingale expression has to be <= 0 eventually
        if not is_invariant(self.martingale_expression, self.program):
            return Result.UNKNOWN

        # Eventually one branch of LG_{i+1} - LG_i has to decrease more or equal than constant
        cases = get_branches_for_expression(sympify(self.program.loop_guard), self.program)
        cases = [simplify(case - sympify(self.program.loop_guard)) for case, _ in cases]
        for case in cases:
            bounds = bound_store.get_bounds_of_expr(case)
            n = symbols('n')
            if is_dominating_or_same(bounds.upper, sympify(-1), n, direction=Direction.NegInf):
                return Result.AST

        return Result.UNKNOWN
