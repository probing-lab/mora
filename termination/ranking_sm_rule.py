"""
This module implements the ranking supermartingale proof rule
"""

from diofant import symbols, limit, oo, sympify
from termination import bound_store
from termination.invariance import is_invariant
from termination.rule import Rule, Result, Witness
from termination.utils import get_max_0, Answer
from termination.asymptotics import is_dominating_or_same, Direction


class RankingSMRule(Rule):

    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        max_0 = get_max_0(self.loop_guard_change, n)
        return bool(lim < 0 or max_0 > 0)

    def run(self, result: Result):
        if result.PAST.is_known():
            return result

        # Martingale expression has to be <= 0 eventually
        if not is_invariant(self.martingale_expression, self.program):
            return result

        # To be ranking martingale expression has to eventually decrease more or equal to constant
        bounds = bound_store.get_bounds_of_expr(self.martingale_expression)
        n = symbols('n')
        if not is_dominating_or_same(bounds.upper, sympify(-1), n, direction=Direction.NegInf):
            return result

        result.PAST = Answer.TRUE
        result.AST = Answer.TRUE
        result.add_witness(PASTWitness(
            self.program.loop_guard,
            self.martingale_expression,
            bounds.upper
        ))

        return result


class PASTWitness(Witness):

    def __init__(self, ranking_martingale, martingale_expression, bound):
        super(PASTWitness, self).__init__("PAST")
        ranking_martingale = sympify(ranking_martingale).as_expr()
        martingale_expression = sympify(martingale_expression).as_expr()
        bound = sympify(bound).as_expr()
        self.data = {
            "Ranking SM": ranking_martingale,
            "SM expression": martingale_expression,
            "SM expression bound": bound,
        }
        self.explanation = f"Eventually, '{ranking_martingale}' is a ranking supermartingale. Thats because eventually\n" \
                           f"the bound of the supermartingale expression is '{bound}'."
