from diofant import Expr, sympify, symbols, reduce_inequalities
from mora.core import Program


def is_invariant(expression: Expr, program: Program, n0: int):
    expression = strap_expression(expression)
    n = symbols('n')
    result = solve_and_simplify([expression > 0, n > n0])
    is_inv = not bool(result)
    return is_inv


def strap_expression(expression: Expr):
    expression = expression.args[0] if len(expression.args) > 0 else expression
    return sympify(str(expression))


def solve_and_simplify(inequalities):
    s = get_first_free_symbol(inequalities)
    result = reduce_inequalities(inequalities, [s])
    return simplify_result(result, s)


def get_first_free_symbol(inequalities):
    for i in inequalities:
        if len(i.free_symbols) > 0:
            return list(i.free_symbols)[0]
    return None


def simplify_result(result, symbol):
    if bool(result) is False:
        return result
    return reduce_inequalities([i for i in result.args], [symbol])
