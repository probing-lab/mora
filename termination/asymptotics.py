from diofant import *
from termination.utils import *


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

    return simplify_asymptotically(result, n)


def __get_eventual_bound(f1: Expr, f2: Expr, n: Symbol, upper: bool = True) -> Expr:
    """
    Given two expressions in n it returns a single expression which is eventually a bound on f1 and f2.
    It does so by investigating the limits of the passed functions as well as the limit of the fraction.
    """
    lower = not upper
    limit_f1 = limit(f1, n, oo)
    limit_f2 = limit(f2, n, oo)

    if not limit_f1.is_infinite and not limit_f2.is_infinite:
        # If both limits are constant we can just compare them. If their comparison doesn't give a boolean,
        # this means they are either both positive or both negative and it doesn't matter which one we return.
        if not (limit_f1 > limit_f2).is_Boolean:
            return limit_f1
        elif (upper and limit_f1 > limit_f2) or (lower and limit_f1 < limit_f2):
            return limit_f1
        else:
            return limit_f2

    # FROM HERE onward: at least one limit is +/- infinity

    if limit_f1 != limit_f2:
        # both functions have different limits, so it is enough to compare the limits
        if (upper and limit_f1 > limit_f2) or (lower and limit_f1 < limit_f2):
            return f1
        else:
            return f2

    # FROM HERE onward: both limits are +/- infinity

    if limit_f1 == oo:
        # if both functions go to +infinity, we have to investigate their fraction
        if (upper and limit(f1 / f2, n, oo) > 0) or (lower and limit(f1 / f2, n, oo) == 0):
            return f1
        else:
            return f2

    if limit_f1 == -oo:
        # if both functions go to -infinity, we have to investigate their fraction
        if (upper and limit(f1 / f2, n, oo) == 0) or (lower and limit(f1 / f2, n, oo) > 0):
            return f1
        else:
            return f2


def simplify_asymptotically(expression: Expr, n: Symbol):
    """
    For a given expression returns another expression such that eventually the two expressions grow/shrink at
    the same rate.
    """
    if n not in expression.free_symbols:
        return expression

    limit_exp = limit(expression, n, oo)
    if limit_exp == 0:
        return expression

    c = unique_symbol('c', positive=True, real=True)
    if limit_exp < 0:
        c = -c

    return c * Order(expression, (n, oo)).expr
