import math
from diofant import solve, Expr, Symbol


def get_max_0(expression: Expr, n: Symbol):
    """
    Returns the maximum 0 of a given expression or 0.
    """
    try:
        zeros = solve(expression, n)
        zeros = [z[n] for z in zeros if z[n].is_real]
    except NotImplementedError:
        zeros = []
    zeros = [math.ceil(float(z)) for z in zeros] + [0]
    return max(zeros)
