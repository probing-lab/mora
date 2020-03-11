"""
This module implements the ranking supermartingale proof rule
"""

from diofant import symbols, limit, oo, sympify
from termination import bound_store
from termination.invariance import is_invariant
from termination.rule import Rule, Result
from termination.utils import get_max_0
from termination.asymptotics import is_dominating_or_same, Direction


class RankingSMRule(Rule):

    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        max_0 = get_max_0(self.loop_guard_change, n)
        return lim < 0 or max_0 > 0

    def run(self):
        # Martingale expression has to be <= 0 eventually
        if not is_invariant(self.martingale_expression, self.program):
            return Result.UNKNOWN

        # To be ranking martingale expression has to eventually decrease more or equal to constant
        bounds = bound_store.get_bounds_of_expr(self.martingale_expression)
        n = symbols('n')
        if not is_dominating_or_same(bounds.upper, sympify(-1), n, direction=Direction.NegInf):
            return Result.UNKNOWN

        return Result.PAST
