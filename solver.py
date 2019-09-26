from diofant import ( symbols, prod, Function, simplify, sympify, rsolve )
from utils import *

def solve_recurrences(recs, rvars, init={}):
    ''' for example, init = {x: 0, y: 0}'''

    def poly2evars(p):
        mono2evar = lambda m: ''.join(str(var) + '^' + str(pow) for var, pow in zip(p.gens, m) if pow)

        poly_over_evars = []
        for c, mono in zip(p.coeffs(), p.monoms()):
            poly_over_evars.append( (c, mono2evar(mono)) )
        return poly_over_evars

    evar_recs = {}
    initial_vals = {} # at iteration 0
    for k, v in recs.items():
        lhs = poly2evars(k.as_poly(rvars))[0][1]##
        ##print('lhs ', lhs)
        rhs = poly2evars(v)
        ##print('rhs ', rhs)
        init_val = k
        ##print('vars:', vars)
        for x in init:
            init_val = init_val.subs({x: EV(init[x])})

        evar_recs[lhs] = rhs
        initial_vals[lhs] = init_val

    fs = {evar: Function(evar) for evar in evar_recs.keys()}
    # iteration/time variable
    n = symbols('n', integer=True)
    solutions = {'': sympify(1)}

    def solve(lhs):
        if lhs in solutions:
            return solutions[lhs]

        print(' Solving for ' + lhs, ' with initial condition {}'.format(str(fs[lhs](0)) + " = " + str(initial_vals[lhs])))

        if lhs in [evar for _, evar in evar_recs[lhs]]: # recurrence
            eqn = fs[lhs](n) - sum( coeff * (solve(evar).subs({n: n-1}) if evar != lhs else fs[lhs](n-1)) for coeff, evar in evar_recs[lhs])
            #print('   equation', eqn)
            ##print('DEBUG ', lhs, initial_vals)
            res = rsolve(eqn, fs[lhs](n), init={fs[lhs](0): initial_vals[lhs]} if initial_vals[lhs] != None else None)

        else: # non recurrence
            res = sum( coeff * solve(evar).subs({n: n-1}) for coeff, evar in evar_recs[lhs])
        solutions[lhs] = res
        print('   ', lhs + '(n)', '   -> ', res)
        return res

    for lhs in evar_recs.keys():
        print('SOLUTION\n  ', lhs, ' = ', simplify(solve(lhs)))
