from diofant import *
from mora.core import Program
from termination.utils import *
from termination.asymptotics import *
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

    expr_bounds.upper = simplify_asymptotically(expr_bounds.upper.as_expr(), symbols('n'))
    expr_bounds.lower = simplify_asymptotically(expr_bounds.lower.as_expr(), symbols('n'))
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
    n = symbols('n')
    structures = structure_store.get_structures_of_evar(evar)
    inhom_parts_bounds = [get_bounds_of_expr(s.inhom_part) for s in structures]
    initial_value = structure_store.get_initial_value_of_evar(evar)
    maybe_pos, maybe_neg = __get_evar_polarity(evar, inhom_parts_bounds, initial_value)

    inhom_parts_bounds_lower = [b.lower.subs({n: n - 1}) for b in inhom_parts_bounds]
    inhom_parts_bounds_upper = [b.upper.subs({n: n - 1}) for b in inhom_parts_bounds]

    max_upper = get_eventual_bound(inhom_parts_bounds_upper, n, upper=True)
    min_lower = get_eventual_bound(inhom_parts_bounds_lower, n, upper=False)
    min_rec = min([s.recurrence_constant for s in structures])
    max_rec = max([s.recurrence_constant for s in structures])
    starting_values = __get_starting_values(maybe_pos, maybe_neg)

    upper_candidates = __compute_bound_candidates({min_rec, max_rec}, {max_upper}, starting_values)
    lower_candidates = __compute_bound_candidates({min_rec, max_rec}, {min_lower}, starting_values)

    max_upper_candidate = get_eventual_bound(upper_candidates, n, upper=True)
    min_lower_candidate = get_eventual_bound(lower_candidates, n, upper=False)

    bounds = Bounds()
    bounds.expression = evar
    bounds.upper = max_upper_candidate.as_expr()
    bounds.lower = min_lower_candidate.as_expr()
    bounds.maybe_positive = maybe_pos
    bounds.maybe_negative = maybe_neg

    store[evar] = bounds


def __get_evar_polarity(evar: Expr, inhom_parts_bounds: [Bounds], initial_value: Number):
    powers = get_all_evar_powers(evar)
    all_powers_even = all([p % 2 == 0 for p in powers])
    if all_powers_even:
        return True, False

    initial_pos = sympify(initial_value) > 0
    if initial_pos.is_Relational:
        initial_pos = True
    else:
        initial_pos = bool(initial_pos)

    initial_neg = sympify(initial_value) < 0
    if initial_neg.is_Relational:
        initial_neg = True
    else:
        initial_neg = bool(initial_neg)

    maybe_pos = initial_pos or any([b.maybe_positive for b in inhom_parts_bounds])
    maybe_neg = initial_neg or any([b.maybe_negative for b in inhom_parts_bounds])
    return maybe_pos, maybe_neg


def __get_starting_values(maybe_pos, maybe_neg):
    values = []
    if maybe_pos:
        values.append(unique_symbol('d', positive=True))
    if maybe_neg:
        values.append(unique_symbol('d', positive=True) * -1)
    if not maybe_pos and not maybe_neg:
        values.append(sympify(0))

    return values


def __compute_bound_candidates(coefficients, inhom_parts, starting_values):
    candidates = []

    for c in coefficients:
        for part in inhom_parts:
            c0 = symbols('c0')
            solution = __compute_bound_candidate(c, part, c0)
            for v in starting_values:
                new_candidates = __split_on_signums(solution.subs({c0: v}))
                candidates += new_candidates

    return candidates


def __compute_bound_candidate(c, inhom_part, starting_value):
    f = Function('f')
    n = symbols('n')
    print("Solving recurrence: ", f(n) - c*f(n-1) - inhom_part)
    solution = rsolve(f(n) - c*f(n-1) - inhom_part, f(n), {f(0): starting_value})
    print("Found solution!")
    return solution


def __split_on_signums(expression: Expr):
    exps = [expression]
    n = symbols('n')
    expression_limit = limit(expression, n, oo)
    signums = get_signums_in_expression(expression_limit)
    for s in signums:
        new_exps = []
        for exp in exps:
            constant = unique_symbol('e', positive=True)
            new_exps.append(exp.subs({s: constant}))
            new_exps.append(exp.subs({s: constant * -1}))
        exps = new_exps
    return exps
