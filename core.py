from diofant import ( symbols, prod, Function, simplify, sympify, rsolve )
from utils import *
from parser import InputParser
from solver import solve_recurrences

prog = InputParser("""x = 0
while true:
    u = RV(uniform, 0, d)
    x = x + u @ 1
    y = y + x - 2*u @ 1""")



def core(prog, goal=2, exact=True):
    """
    INPUT:
    InputParser prog
    exact flag - treat all numbers as rationals

    """
    vars = prog.variables
    rvars = vars[::-1]
    initial = prog.initial_values
    parameters = prog.parameters
    updates = prog.updates

    domain = 'QQ{}'.format(prog.parameters) if exact else 'ZZ'
    goal = prog.goals

    #parameters = ['d l']
    exact = True
    poly_domain = 'QQ{}'.format(parameters) if exact else 'ZZ{}'.format(parameters)

    goal = [vars[-1]**1]
    #  x, y, s = symbols("x y s")
    #  f, u1, u2 = symbols("f u1 u2")
    #  d = symbols("d")
    #  x0 = symbols('x(0)')
    #
    #  vars = [u1, u2, f, x, y, s]
    #  rvars = vars[::-1]
    #  # rank = {x:0, y:1}
    #  initial = {f:0, x:x0, y:0, s:0}
    #  #initial = {f:0, x:x0, y:UniformVar(0, 1), s:0} !!!not ok
    #  parameters = [d]
    #  goal = [s**2]
    #  updates = {
    #          #f : Update(f, "", is_random_var=True, random_var=UniformVar(-1, 1)),
    #          u2 : Update(u2, "", is_random_var=True, random_var=UniformVar(2-2*d, 2+2*d)),
    #          u1 : Update(u1, "", is_random_var=True, random_var=UniformVar(1-d, 1+d)),
    #          f : Update(f, "1 @ 3/4; 0 @ 1/4"),
    #          x : Update(x, "x + f * u1 @ 1"),
    #          y : Update(y, "y + f * u2 @ 1"),
    #          s : Update(s, "s + x * y @ 1")
    #
    #          # x: Update(x, "x + f @ 1"),
    #          # y: Update(x, "y @ 1/2; y + 2*x @ 1/2")
    #      }
    MBRecs = dict()

    S = {g for g in goal}
    while S:
        M = S.pop()
        M_orig = M
        M = M.as_poly(rvars)
        for i, var in enumerate(rvars):
            M = M.as_poly(var)
            terms = [ (coeff*var**mono[0]).as_poly(var) for coeff, mono in zip(M.coeffs(), M.monoms())]
            #print("DEBUG ", var, M)
            for j, term in enumerate(terms):
                #print("  .........   ", term)
                pow = term.monoms()[0][0] # power of var in term
                #terms[j] = updates[var].update_term(term, pow).as_poly(rvars, domain='QQ')

                ##
                terms[j] = updates[var].update_term(term, pow)
                #print("  TADAAAAAA   ", terms[j])
                #print("  TADA        ", term)
                terms[j] = updates[var].update_term(term, pow).as_poly(rvars)
                #print("  DA          ", terms[j])
                ## terms[j] = updates[var].update_term(term, pow).as_poly(rvars, domain=domain)#to include symbolic vars as well, e.g. d in example from intro
            M = sum(terms).as_poly(rvars)
            # print(' var was ', var, '\n  ', M)

        # print(M)
        # import sys; sys.exit(0)
            # M = M.as_poly(var)
            # for mono in M.monoms():
            #     pow = mono[0]
            #     if pow > 0:
            #         M = M.subs({var**pow: updates[var].power(pow)})
            #         M = M.as_poly(rvars)
            #         if M_orig == p:
            #             print(var, ' update na ', M)
        MBRecs[M_orig] = M

        for mono in M.monoms():
            N = prod(v**pow for v, pow in zip(M.gens, mono))
            if N not in MBRecs and N != 1:
                S.add(N)

    print(' --- MBRecs --- ')
    for k, v in MBRecs.items():
        print(' '*3, k, ' = ', v.as_expr())
    print()


    # without initial conditions
    # solve_recurrences(MBRecs, init={})
    # with initial conditions
    solve_recurrences(MBRecs, rvars, init=initial)
