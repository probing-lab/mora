"""
This module contains functions deciding whether or not a given expression is an invariant of the program,
More precisely, it decides whether expression <= 0 is eventually invariant.
The methods are of course not complete in general.
"""
from diofant import Expr, sympify, symbols
from mora.core import Program
from termination import bound_store
from termination.utils import get_max_0
from termination.asymptotics import is_dominating_or_same, Direction
from enum import Enum


class Answer(Enum):
    FALSE = 1
    TRUE = 2
    UNKNOWN = 3

    def to_boolean(self):
        return self is Answer.TRUE

    def is_known(self):
        return self is not Answer.UNKNOWN


def is_invariant(expression: Expr, program: Program) -> bool:
    """
    Main function deciding whether expression <= 0 is eventually invariant
    """
    expression = __strap_expression(expression)
    n = symbols('n')
    is_deterministic = len(expression.free_symbols.difference({n})) == 0
    if is_deterministic:
        return is_deterministic_invariant(expression)
    else:
        return is_probabilistic_invariant(expression, program)


def is_deterministic_invariant(expression: Expr) -> bool:
    """
    Checks whether an expression only containing n eventually stays <= 0
    """
    n = symbols('n')
    max_0 = get_max_0(expression, n)
    return expression.subs({n: max_0 + 1}) <= 0


def is_probabilistic_invariant(expression: Expr, program: Program) -> bool:
    """
    Tries several strategies to determine if a given expression eventually stays <= 0
    """
    answer = __is_probabilistic_invariant_via_bounds(expression)
    if answer.is_known():
        return answer.to_boolean()

    answer = __is_probabilistic_invariant_via_z3(expression, program)
    return answer.to_boolean()


def __is_probabilistic_invariant_via_bounds(expression: Expr) -> Answer:
    """
    Tries to decide if expression <= 0 eventually becomes invariant via bounds.
    """
    n = symbols('n')
    bounds = bound_store.get_bounds_of_expr(expression)
    if is_dominating_or_same(bounds.upper, sympify(-1), n, direction=Direction.NegInf):
        return Answer.TRUE

    if is_dominating_or_same(bounds.lower, sympify(1), n, direction=Direction.PosInf):
        return Answer.FALSE

    return Answer.UNKNOWN


def __is_probabilistic_invariant_via_z3(expression: Expr, program: Program) -> Answer:
    raise NotImplementedError()


def __strap_expression(expression: Expr) -> Expr:
    expression = expression.args[0] if len(expression.args) > 0 else expression
    return sympify(str(expression))
