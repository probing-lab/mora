"""
This module implements the repulsing supermartingale proof rule
"""

from diofant import symbols, limit, oo
from termination.invariance import is_invariant
from termination.rule import Rule, Result


class RepulsingSMRule(Rule):

    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        return lim > 0

    def run(self):
        # TODO check asymptotic behavior (not sound yet)
        # TODO check if pos probability of having next iteration
        if is_invariant(self.martingale_expression, self.program):
            return Result.NONTERM
        return Result.UNKNOWN
