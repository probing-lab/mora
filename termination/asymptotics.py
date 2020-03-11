from diofant import *
from termination.utils import *
from enum import Enum


class Direction(Enum):
    PosInf = 1
    NegInf = 2


def get_eventual_bound(fs: [Expr], n: Symbol, direction: Direction = Direction.PosInf) -> Expr:
    """
    Given a list of expressions in n, it returns a single expression which is eventually a bound on all fs.
    Depending on the 'direction' parameter, the bound is either an eventual upper bound or eventual lower bound.
    """
    result = None
    for f in fs:
        if result is None:
            result = f
        else:
            result = result if is_dominating_or_same(result, f, n, direction) else f

    return simplify_asymptotically(result, n)


def is_dominating_or_same(f1: Expr, f2: Expr, n: Symbol, direction: Direction = Direction.PosInf) -> bool:
    """
    Given two expressions in n it returns True iff the first expression eventually dominates the second one, modulo a
    positive constant factor.
    Whether domination should be considered towards +infinity or -infinity can be changed with the 'direction' parameter.
    """
    upper = direction is Direction.PosInf
    lower = not upper
    limit_f1 = limit(f1, n, oo)
    limit_f2 = limit(f2, n, oo)

    # if both limits are constant
    if not limit_f1.is_infinite and not limit_f2.is_infinite:
        if upper:
            # f1 dominates if it's eventually positive or both are negative
            return limit_f1.is_positive or limit_f2.is_negative
        else:
            # f1 dominates if it's eventually negative or both are positive
            return limit_f1.is_negative or limit_f2.is_positive

    # FROM HERE onward: at least one limit is +/- infinity

    if limit_f1 != limit_f2:
        # both functions have different limits, so it is enough to compare the limits
        return (upper and limit_f1 > limit_f2) or (lower and limit_f1 < limit_f2)

    # FROM HERE onward: both limits are +/- infinity

    if limit_f1 == oo:
        # if both functions go to +infinity, we have to investigate their fraction
        return (upper and limit(f1 / f2, n, oo) > 0) or (lower and limit(f1 / f2, n, oo).is_finite)

    if limit_f1 == -oo:
        # if both functions go to -infinity, we have to investigate their fraction
        return (upper and limit(f1 / f2, n, oo).is_finite) or (lower and limit(f1 / f2, n, oo) > 0)


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
