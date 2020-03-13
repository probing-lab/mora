"""
This module implements the repulsing supermartingale proof rule
"""

from diofant import symbols, limit, oo, sympify, simplify

from termination import bound_store
from termination.asymptotics import get_eventual_bound, is_dominating_or_same, Answer
from termination.expression import get_branches_for_expression
from termination.invariance import is_invariant
from termination.rule import Rule, Result, Witness


class RepulsingSMRule(Rule):

    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        return lim >= 0

    def run(self, result: Result):
        if result.PAST.is_known() and result.AST.is_known():
            return result

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
            result.add_witness(NONASTWitness(
                sympify(self.program.loop_guard) * -1,
                self.martingale_expression,
                epsilons,
                cs
            ))
        elif is_dominating_or_same(epsilons, sympify(0), n) and is_dominating_or_same(sympify(1), cs, n):
            result.PAST = Answer.FALSE
            result.add_witness(NONPASTWitness(
                sympify(self.program.loop_guard) * -1,
                self.martingale_expression
            ))

        return result


class NONASTWitness(Witness):

    def __init__(self, repulsing_martingale, martingale_expression, epsilons, cs):
        super(NONASTWitness, self).__init__("Not AST")
        repulsing_martingale = sympify(repulsing_martingale).as_expr()
        martingale_expression = sympify(martingale_expression).as_expr()
        epsilons = sympify(epsilons).as_expr()
        cs = sympify(cs).as_expr()
        self.data = {
            "Repulsing SM": repulsing_martingale,
            "SM expression": martingale_expression,
            "Epsilons": epsilons,
            "Cs": cs
        }
        self.explanation = f"There is always a positive probability of having a next iteration.\n" \
                           f"Moreover, '{repulsing_martingale}' eventually is a repulsing supermartingale\n" \
                           f"decreasing with epsilons '{epsilons}'. Also, the repulsing SM has differences bound\n" \
                           f"by '{cs}' which is O(epsilons)."


class NONPASTWitness(Witness):

    def __init__(self, repulsing_martingale, martingale_expression):
        super(NONPASTWitness, self).__init__("Not PAST")
        repulsing_martingale = sympify(repulsing_martingale).as_expr()
        martingale_expression = sympify(martingale_expression).as_expr()
        self.data = {
            "Repulsing SM": repulsing_martingale,
            "SM expression": martingale_expression,
        }
        self.explanation = f"There is always a positive probability of having a next iteration.\n" \
                           f"Moreover, '{repulsing_martingale}' eventually is a repulsing supermartingale\n" \
                           f"decreasing with epsilons '0'. Also, the repulsing SM has differences bound\n" \
                           f"by a constant."
