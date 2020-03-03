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
        if (upper and limit(f1 / f2, n, oo) > 0) or (not upper and limit(f1 / f2, n, oo) == 0):
            return f1
        else:
            return f2

    if limit_f1 == -oo:
        # if both functions go to -infinity, we have to investigate their fraction
        if (upper and limit(f1 / f2, n, oo) == 0) or (not upper and limit(f1 / f2, n, oo) > 0):
            return f1
        else:
            return f2

    # Here both f1 and f2 converge to the same real number
    if upper:
        return simplify(limit_f1 + 0.01)
    else:
        return simplify(limit_f1 - 0.01)
