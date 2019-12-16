from diofant import *


def get_expected_loop_guard_change(expected_loop_guard: Expr):
    n = get_n(expected_loop_guard)
    if n is None:
        return Integer(0)

    expected_loop_guard = expected_loop_guard
    shifted_expectation = expected_loop_guard.subs({n: n - 1})
    expected_delta = simplify(expected_loop_guard - shifted_expectation)

    return expected_delta


def get_n(expression: Expr):
    for s in expression.free_symbols:
        if str(s) is "n":
            return s
    return None
