"""
This module contains functions which compute for for a given expression M_{i+1} all possible M_i
which could be the predecessor of M_{i+1} before executing the loop body together with the associated
probabilities.
"""

from diofant import Expr, Symbol, simplify, Rational
from mora.core import Program

# Type aliases to improve readability
Probability = Rational
Case = (Expr, Probability)


def get_expression_pre_loop_body(expression: Expr, program: Program):
    """
    The main funciton computing all possible M_i from M_{i+1} together with the associated probabilites
    """
    result = [(expression, 1)]

    for symbol in reversed(program.variables):
        result = split_expressions_on_symbol(result, symbol, program)
        result = combine_expressions(result)

    return result


def split_expressions_on_symbol(expressions: [Case], symbol: Symbol, program: Program):
    """
    Splits all given expressions on the possibilities of updating a given symbol
    """
    result = []
    for expr, prob in expressions:
        if symbol in program.updates.keys() and symbol in expr.free_symbols:
            for u, p in program.updates[symbol].branches:
                new_expression = simplify(expr.subs({symbol: u}))
                new_prob = prob * p
                result.append((new_expression, new_prob))
        else:
            result.append((expr, prob))

    return result


def combine_expressions(expressions: [Case]):
    """
    In a given list of expressions with probabilities, combines equal expressions and their probabilities
    """
    tmp_map = {}
    for e, p in expressions:
        tmp_map[e] = tmp_map[e] + p if e in tmp_map else p
    return tmp_map.items()
