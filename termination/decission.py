"""
This is the module which handles the decision on what proof-rule to apply to a program in order
to get something about its termination behavior. Then the proof-rule gets applied
"""

from mora.core import Program
from mora.input import LOOP_GUARD_VAR
from diofant import Expr, sympify, simplify, symbols
from .martingale_rule import MartingaleRule
from .ranking_sm_rule import RankingSMRule
from .repulsing_sm_rule import RepulsingSMRule
from .rule import Result

LOOP_GUARD_CHANGE = 'loop_guard_change^1'


def decide_termination(program: Program):
    """
    The main function, gathering all the information, deciding on and calling a proof-rule
    """
    lgc = prepare_loop_guard_change(program)
    me_pos = create_martingale_expression(program, False)
    me_neg = create_martingale_expression(program, True)
    rules = [
        RankingSMRule(lgc, me_pos, program),
        MartingaleRule(lgc, me_pos, program),
        RepulsingSMRule(lgc, me_neg, program)
    ]

    result = Result.UNKNOWN
    for rule in rules:
        if rule.is_applicable():
            result = rule.run()
            if result is not Result.UNKNOWN:
                break

    outputs = {
        Result.UNKNOWN: 'unknown',
        Result.AST: 'AST',
        Result.PAST: 'PAST',
        Result.NONTERM: 'non-terminating',
    }

    print(outputs[result])


def create_martingale_expression(program: Program, invert: bool):
    """
    Creates the martingale expression E(M_{i+1} - M_i | F_i). Also deterministic variables get substituted
    with their representation in n.
    """
    expected_guard = program.recurrences[symbols(LOOP_GUARD_VAR)]
    expression = simplify(expected_guard - sympify(program.loop_guard))

    if invert:
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

    return loop_guard_change


def substitute_deterministic_variables(expr: Expr, program: Program):
    """
    Substitutes deterministic variables in a given expression with their representation in n.
    """
    for symbol, update in program.updates.items():
        if str(symbol) is not LOOP_GUARD_VAR and not update.is_probabilistic:
            expr = expr.subs({symbol: program.moments[str(symbol) + "^1"]})

    return expr
