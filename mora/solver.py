from diofant import symbols, Function, simplify, rsolve
from .utils import *


def solve_recurrences(recs, rvars, init={}):
    ''' for example, init = {x: Update(whatever), y: Update(whateverer)}'''

    def poly2evars(p):
        mono2evar = lambda m: ''.join(str(var) + '^' + str(pow) for var, pow in zip(p.gens, m) if pow)

        poly_over_evars = []
        for c, mono in zip(p.coeffs(), p.monoms()):
            poly_over_evars.append( (c, mono2evar(mono)) )
        return poly_over_evars

    evar_recs = {}
    initial_vals = {} # at iteration 0
    # Get initial value for every E-variable
    for k, v in recs.items():
        lhs = poly2evars(k.as_poly(rvars))[0][1]
        rhs = poly2evars(v)
        init_val = k
        for x in init:
            pow = get_exponent_of(x, init_val)
            if pow>0:
                init_val = init_val.subs({x**pow: init[x].update_term(init_val, pow)})

        evar_recs[lhs] = rhs
        initial_vals[lhs] = init_val

    fs = {evar: Function(evar) for evar in evar_recs.keys()}
    # iteration/time variable
    n = symbols('n', integer=True)
    solutions = {'': sympify(1)}

    def solve(lhs):
        if lhs in solutions:
            return solutions[lhs]

        log(' Solving for ' + lhs, ' with initial condition {}'.format(str(fs[lhs](0)) + " = " + str(initial_vals[lhs])))

        if lhs in [evar for _, evar in evar_recs[lhs]]: # recurrence
            eqn = fs[lhs](n) - sum( coeff * (solve(evar).subs({n: n-1}) if evar != lhs else fs[lhs](n-1)) for coeff, evar in evar_recs[lhs])
            res = rsolve(eqn, fs[lhs](n), init={fs[lhs](0): initial_vals[lhs]})

        else: # non recurrence
            res = sum( coeff * solve(evar).subs({n: n-1}) for coeff, evar in evar_recs[lhs])
        solutions[lhs] = simplify(res)
        log('   ', lhs + '(n)', '   -> ', res)
        return res

    for lhs in evar_recs.keys():
        log(' Solution found\n  ', lhs, ' = ', solve(lhs))

    return solutions
