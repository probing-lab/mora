"""
This module implements the general proof rule for AST
"""

from diofant import limit, symbols, oo, sympify, simplify

from termination import bound_store
from termination.asymptotics import is_dominating_or_same, Direction, Answer
from termination.expression import get_branches_for_expression
from termination.invariance import is_invariant
from termination.rule import Rule, Result, Witness


class MartingaleRule(Rule):
    def is_applicable(self):
        n = symbols('n')
        lim = limit(self.loop_guard_change, n, oo)
        return lim == 0

    def run(self, result: Result):
        if result.AST.is_known():
            return result

        # Martingale expression has to be <= 0 eventually
        if not is_invariant(self.martingale_expression, self.program):
            return result

        # Eventually one branch of LG_{i+1} - LG_i has to decrease more or equal than constant
        cases = get_branches_for_expression(sympify(self.program.loop_guard), self.program)
        for case, prob in cases:
            bounds = bound_store.get_bounds_of_expr(case - sympify(self.program.loop_guard))
            n = symbols('n')
            if is_dominating_or_same(bounds.upper, sympify(-1), n, direction=Direction.NegInf):
                result.AST = Answer.TRUE
                result.add_witness(ASTWitness(
                    self.program.loop_guard,
                    self.martingale_expression,
                    case,
                    bounds.upper,
                    prob
                ))
                return result

        return result


class ASTWitness(Witness):

    def __init__(self, martingale, martingale_expression, decreasing_branch, bound, prob):
        super(ASTWitness, self).__init__("AST")
        martingale = sympify(martingale).as_expr()
        martingale_expression = sympify(martingale_expression).as_expr()
        decreasing_branch = sympify(decreasing_branch).as_expr()
        bound = sympify(bound).as_expr()
        self.data = {
            "SM": martingale,
            "SM expression": martingale_expression,
            "Decreasing branch": decreasing_branch,
            "Branch change bound": bound,
            "Probability": prob
        }
        self.explanation = f"Eventually, '{martingale}' is a supermartingale. Also eventually, taking the branch\n" \
                           f"'{decreasing_branch}' (which happens with probability {prob}) " \
                           f"changes the supermartingale by at least {bound}."
