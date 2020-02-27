from random import random

from diofant import *
from mora.core import Program
from termination.utils import get_monoms, get_polarity

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
        __compute_bounds(evar)
    return store[evar]


def __compute_bounds(evar: Expr):
    # TODO
    bounds = Bounds()
    bounds.expression = evar
    bounds.lower = sympify(1)
    bounds.upper = sympify(2)
    bounds.maybe_positive = random() > 0.5
    bounds.maybe_negative = random() > 0.5
    store[evar] = bounds
