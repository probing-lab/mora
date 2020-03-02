from random import random

from diofant import *
from mora.core import Program
from termination.utils import *
import termination.structure_store as structure_store

store = {}
program = None


class Bounds:
    expression: Poly
    lower: Expr
    upper: Expr
    maybe_positive: bool
    maybe_negative: bool


def set_program(p: Program):
    """
    Set the program and initialize the store. This function needs to be called before the store is used.
    """
    global program, store
    program = p
    store = {}


def get_bounds_of_expr(expression: Expr) -> Bounds:
    expression = sympify(expression)
    variables = set(program.variables).difference({symbols('n')})
    expression = expression.as_poly(variables)
    expr_bounds = __initialize_bounds_for_expression(expression)
    monoms = get_monoms(expression)
    for evar in monoms:
        evar_bounds = __get_bounds_of_evar(evar)
        __replace_evar_in_expr_bounds(evar, evar_bounds, expression, expr_bounds)

    expr_bounds.upper = expr_bounds.upper.as_expr()
    expr_bounds.lower = expr_bounds.lower.as_expr()
    return expr_bounds


def __replace_evar_in_expr_bounds(evar, evar_bounds: Bounds, expression: Poly, expr_bounds: Bounds):
    coeff = expression.coeff_monomial(evar)
    if coeff > 0:
        upper = evar_bounds.upper
        lower = evar_bounds.lower
        pos = evar_bounds.maybe_positive
        neg = evar_bounds.maybe_negative
    else:
        upper = evar_bounds.lower
        lower = evar_bounds.upper
        pos = evar_bounds.maybe_negative
        neg = evar_bounds.maybe_positive

    expr_bounds.upper = expr_bounds.upper.subs({evar: upper})
    expr_bounds.lower = expr_bounds.lower.subs({evar: lower})
    expr_bounds.maybe_positive = expr_bounds.maybe_positive or pos
    expr_bounds.maybe_negative = expr_bounds.maybe_negative or neg


def __initialize_bounds_for_expression(expression: Poly) -> Bounds:
    bounds = Bounds()
    bounds.expression = expression
    bounds.lower = expression.copy()
    bounds.upper = expression.copy()

    n_expr = expression.coeff_monomial(1)
    pos, neg = get_polarity(n_expr, symbols('n'))

    bounds.maybe_positive = pos
    bounds.maybe_negative = neg
    return bounds


def __get_bounds_of_evar(evar: Expr) -> Bounds:
    evar = sympify(evar)
    if evar not in store:
        __compute_bounds_of_evar(evar)
    return store[evar]


def __compute_bounds_of_evar(evar: Expr):
    structures = structure_store.get_structures_of_evar(evar)
    inhom_parts_bounds = [get_bounds_of_expr(s.inhom_part) for s in structures]
    initial_value = structure_store.get_initial_value_of_evar(evar)
    maybe_pos, maybe_neg = __get_evar_polarity(inhom_parts_bounds, initial_value)

    inhom_parts_bounds_lower = [b.lower for b in inhom_parts_bounds]
    inhom_parts_bounds_upper = [b.upper for b in inhom_parts_bounds]

    n = symbols('n')
    max_upper = get_eventual_bound(inhom_parts_bounds_upper, n, upper=True)
    min_lower = get_eventual_bound(inhom_parts_bounds_lower, n, upper=False)
    min_rec = min([s.recurrence_constant for s in structures])
    max_rec = max([s.recurrence_constant for s in structures])

    bound_candidates = __compute_bound_candidates({min_rec, max_rec}, {max_upper, min_lower})

    pass


def __get_evar_polarity(inhom_parts_bounds: [Bounds], initial_value: Number):
    initial_pos = not (initial_value <= 0)
    initial_neg = not (initial_value >= 0)
    maybe_pos = initial_pos or any([b.maybe_positive for b in inhom_parts_bounds])
    maybe_neg = initial_neg or any([b.maybe_negative for b in inhom_parts_bounds])
    return maybe_pos, maybe_neg


def __compute_bound_candidates(coefficients, inhom_parts):
    candidates = []

    for c in coefficients:
        for part in inhom_parts:
            candidates.append(__compute_bound_candidate(c, part))

    return candidates


def __compute_bound_candidate(c, inhom_part):
    f = Function('f')
    n = symbols('n')
    c0 = symbols('c0')
    solution = rsolve(f(n) - c*f(n-1) - inhom_part, f(n), {f(0): c0})
    return solution
