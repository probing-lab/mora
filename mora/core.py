from diofant import  Symbol, sympify, simplify, Expr, Poly
from mora.utils import Update, monomial_is_constant, get_monoms
from typing import List, Dict


class Program:
    def __init__(self):
        self.name: str = ""
        self.source: str = ""
        self.variables: List[Symbol] = []
        self.initial_values: Dict[Symbol, Update] = {}
        self.updates: Dict[Symbol, Update] = {}
        self.goals: List[int] = []


store = {}


def core(program: Program, goal_monomials: List[Expr] = None, goal_power: int = 1):
    """
    Returns the expected values of given monomials raised to a given power. If no monomials are given the expected
    values of all program variables get computed.
    """
    if goal_monomials is None:
        goal_monomials = [v**goal_power for v in program.variables]

    goal_monomials = [m.as_poly(program.variables) for m in goal_monomials]
    solutions = {}
    for m in goal_monomials:
        solutions[m] = get_solution(program, m)
    return solutions


def get_solution(program: Program, monomial: Poly):
    """
    For a given monomial returns its expected value by first checking if it already has been computed and stored
    """
    global store
    if monomial_is_constant(monomial):
        return monomial
    if monomial not in store:
        store[monomial] = compute_solution(program, monomial)
    return store[monomial]


def compute_solution(program: Program, monomial: Poly):
    """
    For a given monomial returns its expected value by constructing and solving a recurrence relation
    """
    monomial = replace_rvs_in_polynomial(program, monomial)
    if monomial_is_constant(monomial):
        return monomial

    factor = monomial.coeffs()[0]
    monomial = monomial.monic()
    expected_post_loop_body = get_expected_post_loop_body(program, monomial)
    recurr_coeff = expected_post_loop_body.coeff_monomial(monomial.as_expr())
    inhom_part = expected_post_loop_body - (recurr_coeff * monomial)
    # TODO: solve inhom part recursively
    # TODO: get initial value of monomial
    # TODO: solve reucrrence relation
    return sympify(1)


def get_expected_post_loop_body(program: Program, monomial: Poly):
    """
    For a given monomial m returns E[ m_{n+1} | F_n ]
    """
    branches = [(monomial.copy(), 1)]
    for variable in monomial.as_expr().free_symbols:
        if variable in program.updates:
            branches_new = []
            for branch, prob in branches:
                for b, p in program.updates[variable].branches:
                    branches_new.append((branch.subs({variable: b}), prob * p))
            branches = branches_new

    expected = sympify(0)
    for branch, prob in branches:
        expected += prob * branch

    loop_body = simplify(expected).as_poly(program.variables)
    loop_body = replace_rvs_in_polynomial(program, loop_body)
    return loop_body


def replace_rvs_in_polynomial(program: Program, polynomial: Poly):
    """
    For a given polynomial return a polynomial such that all powers of random variables are replaced with their
    corresponding moments.
    """
    monoms = get_monoms(polynomial)
    for monomial in monoms:
        powers = monomial.monoms()[0]
        vars_with_powers = [(var, power) for var, power in zip(monomial.gens, powers)]
        for variable, power in vars_with_powers:
            if power > 0 and variable in program.updates and program.updates[variable].is_random_var:
                rv = program.updates[variable].random_var
                moment = rv.compute_moment(power)
                polynomial = polynomial.as_expr().subs({variable ** power: moment}).as_poly(program.variables)
    return polynomial
