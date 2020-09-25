from diofant import Symbol, sympify, simplify, Expr, Poly, Function, symbols, rsolve
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
    return store


def get_solution(program: Program, monomial: Poly):
    """
    For a given monomial returns its expected value by first checking if it already has been computed and stored
    """
    global store
    if monomial_is_constant(monomial):
        return monomial.as_expr()
    if monomial not in store:
        store[monomial] = compute_solution(program, monomial)
    return store[monomial]


def compute_solution(program: Program, monomial: Poly):
    """
    For a given monomial returns its expected value by constructing and solving a recurrence relation
    """
    monomial = replace_rvs_in_polynomial(program, monomial)
    if monomial_is_constant(monomial):
        return monomial.as_expr()

    factor = monomial.coeffs()[0]
    monomial = monomial.monic()
    expected_post_loop_body = get_expected_post_loop_body(program, monomial)
    recurr_coeff = expected_post_loop_body.coeff_monomial(monomial.as_expr())
    inhom_part = expected_post_loop_body - (recurr_coeff * monomial)
    inhom_part_solution = get_inhom_part_solution(program, inhom_part)
    initial_value = get_expected_initial_value(program, monomial)
    print(f"Computing solution for { monomial.as_expr() }")
    solution = compute_solution_for_recurrence(recurr_coeff, inhom_part_solution, initial_value)
    print(f"Found solution for { monomial.as_expr() }")
    return factor * solution


def get_inhom_part_solution(program: Program, inhom_part: Poly):
    """
    For a given inhomogenous part of the assignment of a monomial replace the monomials in the inhom part by their
    closed form solutions.
    """
    monomials = get_monoms(inhom_part)
    inhom_part = inhom_part.as_expr()
    replacements = {}
    for monomial in monomials:
        solution = get_solution(program, monomial)
        monomial = monomial.as_expr()
        replacements[monomial] = solution
    return inhom_part.subs(replacements)


def get_expected_initial_value(program: Program, monomial: Poly):
    """
    For a given monomial computes the expected initial value
    """
    powers = monomial.monoms()[0]
    vars_with_powers = [(var, power) for var, power in zip(monomial.gens, powers)]
    result = sympify(1)
    for variable, power in vars_with_powers:
        if power > 0 and variable in program.initial_values:
            if program.initial_values[variable].is_random_var:
                # Variable initialized with RV
                result *= program.initial_values[variable].random_var.compute_moment(power)
            else:
                # Variable initialized with branches
                result *= sum([b[1] * (b[0]**power) for b in program.initial_values[variable].branches])
    return result


def compute_solution_for_recurrence(recurr_coeff: Expr, inhom_part_solution: Expr, initial_value: Expr):
    """
    Computes the (unique) solution to the recurrence relation:
    f(0) = initial_value; f(n) = recurr_coeff * f(n-1) + inhom_part_solution
    """
    if recurr_coeff.is_zero:
        return inhom_part_solution
    f = Function('f')
    n = symbols('n', integer=True)
    solution = rsolve(f(n + 1) - recurr_coeff * f(n) - inhom_part_solution, f(n), init={f(0): initial_value})
    solution = solution[0][f](n)
    return solution


def get_expected_post_loop_body(program: Program, monomial: Poly):
    """
    For a given monomial m returns E[ m_{n+1} | F_n ]
    """
    print(f"LOOP BODY - Computing for {monomial.as_expr()}")
    branches = [(monomial.as_expr(), 1)]
    dependent_symbols = monomial.as_expr().free_symbols
    for variable, update in reversed(program.updates.items()):
        if update.is_random_var:
            continue
        if variable not in dependent_symbols:
            continue
        branches_new = []
        for branch, prob in branches:
            for b, p in program.updates[variable].branches:
                dependent_symbols = dependent_symbols.union(b.free_symbols)
                branches_new.append((branch.subs({variable: b}), prob * p))
        branches = branches_new

    expected = sum([prob * branch for branch, prob in branches])
    loop_body = expected.as_poly(program.variables)
    loop_body = replace_rvs_in_polynomial(program, loop_body)
    return loop_body


def replace_rvs_in_polynomial(program: Program, polynomial: Poly):
    """
    For a given polynomial return a polynomial such that all powers of random variables are replaced with their
    corresponding moments.
    """
    monoms = get_monoms(polynomial)
    replacements = {}
    for monomial in monoms:
        powers = monomial.monoms()[0]
        vars_with_powers = [(var, power) for var, power in zip(monomial.gens, powers)]
        for variable, power in vars_with_powers:
            if power > 0 and variable in program.updates and program.updates[variable].is_random_var:
                rv = program.updates[variable].random_var
                moment = rv.compute_moment(power)
                replacements[variable ** power] = moment
    polynomial = polynomial.as_expr().subs(replacements).as_poly(program.variables)
    return polynomial
