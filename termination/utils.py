import math
from diofant import *


def get_max_0(expression: Expr, n: Symbol):
    """
    Returns the maximum 0 of a given expression or 0.
    """
    try:
        exp_zeros = solve(expression, n)
        exp_zeros = [z[n] for z in exp_zeros if z[n].is_real]
    except NotImplementedError:
        exp_zeros = []
    exp_zeros = [math.ceil(float(z)) for z in exp_zeros] + [0]
    return max(exp_zeros)


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


def get_eventual_bound(fs: [Expr], n: Symbol, upper: bool = True) -> Expr:
    """
    Given a list of expressions in n, it returns a single expression which is eventually a bound on all fs.
    Depending on the 'upper' parameter, the bound is either an eventual upper bound or eventual lower bound.
    """
    result = None
    for f in fs:
        if result is None:
            result = f
        else:
            result = __get_eventual_bound(result, f, n, upper=upper)

    return result


def __get_eventual_bound(f1: Expr, f2: Expr, n: Symbol, upper: bool = True) -> Expr:
    """
    Given two expressions in n it returns a single expression which is eventually a bound on f1 and f2.
    It does so by investigating the limits of the passed functions as well as the limit of the fraction.
    """
    limit_f1 = limit(f1, n, oo)
    limit_f2 = limit(f2, n, oo)

    if limit_f1 != limit_f2:
        # both functions have different limits, so it is enough to compare the limits
        if (upper and limit_f1 > limit_f2) or (not upper and limit_f1 < limit_f2):
            return f1
        else:
            return f2

    if limit_f1 == oo:
        # if both functions go to +infinity, we have to investigate their fraction
        if (upper and limit(f1 / f2, n, oo) > 1) or (not upper and limit(f1 / f2, n, oo) < 1):
            return f1
        else:
            return f2

    if limit_f1 == -oo:
        # if both functions go to -infinity, we have to investigate their fraction
        if (upper and limit(f1 / f2, n, oo) < 1) or (not upper and limit(f1 / f2, n, oo) > 1):
            return f1
        else:
            return f2

    # Here both f1 and f2 converge to the same real number
    if upper:
        return simplify(limit_f1 + 0.01)
    else:
        return simplify(limit_f1 - 0.01)
