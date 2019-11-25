from diofant import *


def get_expected_loop_condition_change(expected_loop_condition: Expr):
    n = get_n(expected_loop_condition)
    if n is None:
        return Integer(0)

    expected_loop_condition = expected_loop_condition
    shifted_expectation = expected_loop_condition.subs({n: n-1})
    expected_delta = simplify(expected_loop_condition - shifted_expectation)

    if expected_delta.is_polynomial():
        expected_delta = expected_delta.as_poly()

    return expected_delta


def get_n(expression: Expr):
    for s in expression.free_symbols:
        if str(s) is "n":
            return s
    return None
