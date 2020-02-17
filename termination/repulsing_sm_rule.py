"""
This module implements the repulsing supermartingale proof rule
"""

from diofant import symbols, limit, oo
from termination.invariance import is_invariant
from termination.rule import Rule, Result


class RepulsingSMRule(Rule):

    def is_applicable(self):
        n = symbols('n', real=True)
        lim = limit(self.loop_guard_change, n, oo)
        return lim > 0

    def run(self):
        # TODO check asymptotic behavior (not sound yet)
        if is_invariant(self.martingale_expression, self.program):
            return Result.NONTERM
        return Result.UNKNOWN
