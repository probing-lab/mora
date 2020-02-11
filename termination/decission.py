"""
This is the module which handles the decision on what proof-rule to apply to a program in order
to get something about its termination behavior. Then the proof-rule gets applied
"""

from mora.core import Program
from mora.input import LOOP_GUARD_VAR
from diofant import Expr, Symbol, sympify, simplify, limit, symbols, oo, solve, diff
import math

LOOP_GUARD_CHANGE = 'loop_guard_change^1'


def decide_termination(program: Program):
    """
    The main function, gathering all the information, deciding on and calling a proof-rule
    """

    loop_guard_change, n = prepare_loop_guard_change(program)
    lim = limit(loop_guard_change, n, oo)
    martingale_expression = create_martingale_expression(program, lim)
    n0 = prepare_n0(loop_guard_change, n)

    print(martingale_expression)
    print(n0)

    # -guard cannot be a supermartingale. Therefore try proving PAST/AST
    if lim < 0:
        print("limit < 0")

    # guard cannot be a supermartingale. Therefore try proving non-termination
    elif lim > 0:
        print("limit > 0")

    # Neither guard nor -guard can be ranking, but guard can be a martingale.
    # Therefore try proving AST
    else:
        print("limit = 0")


def prepare_n0(loop_guard_change: Expr, n: Symbol):
    """
    Takes the loop-guard change and returns the minimum number n0 such that for all n < n0, the loop-guard cannot
    be a supermartingale. So the supermartingale condition, needs only be checked after n0.
    """
    diff_loop_guard_change = diff(loop_guard_change, n)
    try:
        zeros = solve(loop_guard_change, n) + solve(diff_loop_guard_change, n)
    except NotImplementedError:
        zeros = []

    zeros = [math.ceil(float(z[n])) for z in zeros] + [0]
    return max(zeros)


def create_martingale_expression(program: Program, lim: Expr):
    """
    Creates the martingale expression E(M_{i+1} - M_i | F_i). Also deterministic variables get substituted
    with their representation in n.
    """
    expected_guard = program.recurrences[symbols(LOOP_GUARD_VAR)]
    expression = simplify(expected_guard - sympify(program.loop_guard))

    if lim > 0:
        expression *= -1

    expression = simplify(expression)
    expression = substitute_deterministic_variables(expression, program)
    return simplify(expression)


def prepare_loop_guard_change(program: Program):
    """
    Prepares the loop-guard-change for analytic operations by considering the variable as real valued.
    """
    loop_guard_change = program.moments[LOOP_GUARD_CHANGE]
    n_int = symbols('n', integer=True)
    n = symbols('n', real=True)
    loop_guard_change = loop_guard_change.subs({n_int: n})

    return loop_guard_change, n


def substitute_deterministic_variables(expr: Expr, program: Program):
    """
    Substitutes deterministic variables in a given expression with their representation in n.
    """
    for symbol, update in program.updates.items():
        if str(symbol) is not LOOP_GUARD_VAR and not update.is_probabilistic:
            expr = expr.subs({symbol: program.moments[str(symbol) + "^1"]})

    return expr
