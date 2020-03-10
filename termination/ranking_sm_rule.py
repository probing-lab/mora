"""
This module implements the ranking supermartingale proof rule
"""

from diofant import symbols, limit, oo

from termination import bound_store
from termination.invariance import is_invariant
from termination.rule import Rule, Result
from termination.utils import get_max_0


class RankingSMRule(Rule):

    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        max_0 = get_max_0(self.loop_guard_change, n)
        return lim < 0 or max_0 > 0

    def run(self):
        # TODO check asymptotic behavior (not sound yet)
        if is_invariant(self.martingale_expression, self.program):
            bounds = bound_store.get_bounds_of_expr(self.martingale_expression)
            print("Upper bound RSM expression: ", bounds.upper)
            return Result.PAST
        return Result.UNKNOWN
