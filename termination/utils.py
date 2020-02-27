import math
from diofant import solve, Expr, Symbol, Poly, prod, simplify


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


def get_monoms(poly: Poly):
    """
    Returns for the list of monoms for a given polynomial
    """
    monoms = []
    for powers in poly.monoms():
        m = prod(var ** power for var, power in zip(poly.gens, powers))
        if m != 1:
            monoms.append(m)
    return monoms


def get_polarity(expression: Expr, n: Symbol):
    """
    Given an expression in n, returns whether or not the expression is positive and negative for some values of n
    """
    expression = simplify(expression)
    if expression.is_number:
        return expression > 0, expression < 0

    max_0 = get_max_0(expression, n)
    if max_0 > 0:
        pos = True
        neg = True
    else:
        expr_1 = expression.subs({n: 1})
        pos = expr_1 > 0
        neg = expr_1 < 0

    return pos, neg
