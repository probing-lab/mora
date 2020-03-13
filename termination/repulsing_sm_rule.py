"""
This module implements the repulsing supermartingale proof rule
"""

from diofant import symbols, limit, oo, sympify, simplify

from termination import bound_store
from termination.asymptotics import get_eventual_bound, is_dominating_or_same, Answer
from termination.expression import get_branches_for_expression
from termination.invariance import is_invariant
from termination.rule import Rule, Result


class RepulsingSMRule(Rule):

    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        return lim >= 0

    def run(self, result: Result):
        # Martingale expression has to be <= 0 eventually
        if not is_invariant(self.martingale_expression, self.program):
            return result

        cases = get_branches_for_expression(sympify(self.program.loop_guard), self.program)
        cases = [simplify(case - sympify(self.program.loop_guard)) for case, _ in cases]
        cases_bounds = [bound_store.get_bounds_of_expr(case) for case in cases]

        # Make sure that there is always a positive probability of having a next iteration
        if all([cb.maybe_negative for cb in cases_bounds]):
            return result

        n = symbols('n')
        cs = get_eventual_bound([cb.absolute_upper for cb in cases_bounds], n)
        epsilons = simplify(bound_store.get_bounds_of_expr(self.martingale_expression).lower * -1)

        # The epsilons have to grow more or equal to the cs
        if is_dominating_or_same(epsilons, cs, n):
            result.PAST = Answer.FALSE
            result.AST = Answer.FALSE
        elif is_dominating_or_same(epsilons, sympify(0), n) and is_dominating_or_same(sympify(1), cs, n):
            result.PAST = Answer.FALSE

        return result
