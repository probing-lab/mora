from diofant import ( symbols, prod, Function, simplify, sympify, rsolve )
from utils import *
from parser import InputParser
from solver import solve_recurrences


def core(prog, goal=1, exact=True):
    """
    INPUT:
    InputParser prog
    int goal
    """
    vars = prog.variables
    rvars = vars[::-1]
    initial = prog.initial_values
    parameters = prog.parameters
    updates = prog.updates

    S = set_goal(goal, vars)
    poly_domain = 'QQ{}'.format(parameters) if exact else 'ZZ{}'.format(parameters)

    MBRecs = dict()
    while S:
        M = S.pop()
        M_orig = M
        M = M.as_poly(rvars)
        for i, var in enumerate(rvars):
            M = M.as_poly(var)
            terms = [ (coeff*var**mono[0]).as_poly(var) for coeff, mono in zip(M.coeffs(), M.monoms())]
            for j, term in enumerate(terms):
                pow = term.monoms()[0][0] # power of var in term
                terms[j] = updates[var].update_term(term, pow).as_poly(rvars)
            M = sum(terms).as_poly(rvars)

        MBRecs[M_orig] = M

        for mono in M.monoms():
            N = prod(v**pow for v, pow in zip(M.gens, mono))
            if N not in MBRecs and N != 1:
                S.add(N)

    print(' --- MBRecs --- ')
    for k, v in MBRecs.items():
        print(' '*3, k, ' = ', v.as_expr())
    print()

    solve_recurrences(MBRecs, rvars, init=initial)

def set_goal(goal, vars):
    if type(goal)==int:
        S = {x**goal for x in vars}
        return S
