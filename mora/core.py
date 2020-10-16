from diofant import Symbol, sympify, simplify, Expr, Poly, Function, symbols, rsolve
from mora.utils import Update, monomial_is_constant, get_monoms, is_independent_from_all
from typing import List, Dict, Set, Iterable


class Program:
    def __init__(self):
        self.name: str = ""
        self.source: str = ""
        self.variables: List[Symbol] = []
        self.initial_values: Dict[Symbol, Update] = {}
        self.updates: Dict[Symbol, Update] = {}
        self.ancestors: Dict[Symbol, Set[Symbol]] = {}
        self.dependencies: Dict[Symbol, Set[Symbol]] = {}


# Stores the solutions of E-variables
solution_store = {}

# Stores the recurrences of E-variables
recurrence_store = {}


def core(program: Program, goal_monomials: List[Expr] = None, goal_power: int = 1):
    """
    Returns the expected values of given monomials raised to a given power. If no monomials are given the expected
    values of all program variables get computed.
    """
    global solution_store, recurrence_store
    solution_store = {}
    recurrence_store = {}
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
    global solution_store
    if monomial_is_constant(monomial):
        return monomial.as_expr()
    if monomial.as_expr() not in solution_store:
        solution_store[monomial.as_expr()] = compute_solution(program, monomial)
    return solution_store[monomial.as_expr()]


def compute_solution(program: Program, monomial: Poly):
    """
    For a given monomial returns its expected value by constructing and solving a recurrence relation
    """
    monomial = replace_rvs_in_polynomial(program, monomial)
    if monomial_is_constant(monomial):
        return monomial.as_expr()

    factor = monomial.coeffs()[0]
    monomial = monomial.monic()
    recurrence = get_recurrence(program, monomial)
    recurr_coeff = recurrence.coeff_monomial(monomial.as_expr())
    inhom_part = recurrence - (recurr_coeff * monomial)
    inhom_part_solution = get_inhom_part_solution(program, inhom_part)
    initial_value = get_expected_initial_value(program, monomial)
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
    return inhom_part.xreplace(replacements)


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
    f(0) = initial_value; f(n+1) = recurr_coeff * f(n) + inhom_part_solution
    """
    f = Function('f')
    n = symbols('n')
    if recurr_coeff.is_zero:
        return simplify(inhom_part_solution.xreplace({n: n-1}))
    inhom_part_solution = simplify(inhom_part_solution)
    solution = rsolve(f(n + 1) - recurr_coeff * f(n) - inhom_part_solution, f(n), init={f(0): initial_value})
    solution = solution[0][f](n)
    return solution


def get_recurrence(program: Program, monomial: Poly):
    """
    For a given monomial returns its recurrence representation by first checking if it already
    as been computed and stored
    """
    global recurrence_store
    if monomial_is_constant(monomial):
        return monomial
    if monomial.as_expr() not in recurrence_store:
        recurrence_store[monomial.as_expr()] = compute_recurrence(program, monomial)
    return recurrence_store[monomial.as_expr()]


def compute_recurrence(program: Program, monomial: Poly):
    """
    Computes the recurrence of a given monomial by splitting all variables which are dependent with the monomial
    and substitute the solution for variables/monomials which are independent
    """
    recurrence, last_variable = resolve_dependent_variables(program, monomial)
    recurrence = recurrence.as_poly(program.variables)
    recurrence = replace_rvs_in_polynomial(program, recurrence)
    remaining_variables = program.variables[0:program.variables.index(last_variable)]

    if remaining_variables:
        n = symbols('n')
        recurrence = recurrence.as_poly(remaining_variables)
        monoms = get_monoms(recurrence)
        new_recurrence = recurrence.coeff_monomial(1)
        for monomial in monoms:
            coeff = recurrence.coeff_monomial(monomial.as_expr())
            monomial_solution = get_solution(program, monomial.as_poly(program.variables))
            new_recurrence += coeff * monomial_solution.xreplace({n: n + 1})
        recurrence = new_recurrence

    return recurrence.as_poly(program.variables)


def resolve_dependent_variables(program: Program, monomial: Poly):
    """
    Iteratively splits a monomial on variables which are dependent with respect to the given monomial
    """
    result = monomial.as_expr()
    powers = monomial.monoms()[0]
    monom_variables = set([var for var, power in zip(monomial.gens, powers) if power > 0])
    force_next_split = len(monom_variables) == 1
    last_variable = None
    for variable, update in reversed(program.updates.items()):
        if update.is_random_var:
            continue
        if variable not in result.free_symbols:
            continue
        if not force_next_split:
            result = presolve_independent_occurences(program, variable, result)
        else:
            force_next_split = False
        branches = split_expression_on_variable(program, result, variable)
        result = sum([prob * branch for branch, prob in branches])
        result = simplify(result)

        last_variable = variable
        if variable in monom_variables:
            monom_variables.remove(variable)
        # If all variables in the monomial have been considered only independent variables would remain, so stop.
        if not monom_variables:
            break
    return result, last_variable


def split_expression_on_variable(program: Program, expression, variable):
    """
    For a given expression, splits it with the updates of a given variable.
    """
    if variable not in expression.free_symbols:
        return [(expression, sympify(1))]

    branches = []
    for b, p in program.updates[variable].branches:
        branches.append((expression.xreplace({variable: b}), p))
    return branches


def presolve_independent_occurences(program, variable, result):
    n = symbols('n')
    result = result.as_poly(program.variables)
    new_result = result.coeff_monomial(1)
    monoms = get_monoms(result)
    for monom in monoms:
        powers = monom.monoms()[0]
        powers_for_var = {var: power for var, power in zip(monom.gens, powers) if power > 0}
        other_vars = {v for v in powers_for_var.keys() if v != variable}

        if variable not in powers_for_var.keys():
            new_result += result.coeff_monomial(monom.as_expr()) * monom.as_expr()
            continue

        if not is_independent_from_all(program, variable, other_vars):
            new_result += result.coeff_monomial(monom.as_expr()) * monom.as_expr()
            continue

        m = variable ** powers_for_var[variable]
        independent_solution = get_solution(program, m.as_poly(program.variables)).xreplace({n: n+1})
        new_result += result.coeff_monomial(monom.as_expr()) * monom.as_expr().xreplace({m: independent_solution})

    return new_result.as_poly(program.variables)


def replace_rvs_in_polynomial(program: Program, polynomial: Poly):
    """
    For a given polynomial return a polynomial such that all powers of random variables are replaced with their
    corresponding moments.
    """
    monoms = get_monoms(polynomial)
    replacements = {}
    for monomial in monoms:
        powers = monomial.monoms()[0]
        vars_with_powers = [(var, power) for var, power in zip(monomial.gens, powers) if power > 0]
        for variable, power in vars_with_powers:
            if variable in program.updates and program.updates[variable].is_random_var:
                rv = program.updates[variable].random_var
                moment = rv.compute_moment(power)
                replacements[variable ** power] = moment
    polynomial = polynomial.as_expr().xreplace(replacements).as_poly(program.variables)
    return polynomial
