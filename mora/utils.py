from typing import Iterable

from diofant import sympify, Rational, Poly, prod, Symbol
from scipy.stats import norm
from math import sqrt
import re


class Update:
    # parse updates
    # takes string "x = P @ p; Q @ q" or x = RV(d, a, b)
    # creates class to deal with substituing powers of variables and moments
    def __init__(self, var, update_string, is_random_var=False, random_var=None):
        self.is_random_var = is_random_var
        self.random_var = random_var
        self.var = var

        # check if this is a RV or expression update
        rv = re.search(r"RV\((?P<params>.+)\)", update_string)
        if rv is not None:
            self.is_random_var = True
            dist, *params = map(str.strip, rv.group('params').split(','))
            params = list(map(sympify, params))
            self.random_var = RandomVar(dist, params, var_name=str(self.var))

        # here: if not is_random_var == else
        if not self.is_random_var:
            self.branches = []
            branches = update_string.split(";")
            for update in branches:
                if '@' in update:
                    exp, prob = update.split("@")
                else:
                    exp, prob = update, 1-sum([b[1] for b in self.branches])
                prob = sympify(prob)
                if prob.is_Float:
                    prob = Rational(str(prob))
                if not prob.is_zero:
                    self.branches.append((sympify(exp), prob))
            if sum([b[1] for b in self.branches]) != 1:
                raise Exception(f"Branch probabilities for {self.var} update do not sum up to 1. Terminating.")

    def update_term(self, term, pow):
        if self.is_random_var:
            return term.subs({self.var**pow: self.random_var.compute_moment(pow) })
        else:
            return term.subs({self.var**pow: self.power(pow)})

    def power(self, k):
        return sum(prob * (exp ** k) for exp, prob in self.branches)


class RandomVar:
    def __init__(self, distribution, parameters, var_name=None):
        self.distribution = distribution
        self.parameters = parameters
        self.var_name = var_name

    def compute_moment(self, k):
        if self.distribution == 'finite':
            return sum([p * (b ** k) for b, p in self.parameters])

        if self.distribution == 'uniform':
            l, u = self.parameters
            return (u**(k+1)-l**(k+1))/((k+1)*(u-l))

        if self.distribution == 'gauss' or self.distribution == 'normal':
            mu, sigma_squared = self.parameters
            # For low moments avoid scipy.stats.moments as it does not support
            # parametric parameters. In the future get all moments directly,
            # using the following properties:
            # https://math.stackexchange.com/questions/1945448/methods-for-finding-raw-moments-of-the-normal-distribution
            if k == 0:
                return 1
            elif k == 1:
                return mu
            elif k == 2:
                return mu**2 + sigma_squared
            elif k == 3:
                return mu*(mu**2 + 3*sigma_squared)
            elif k == 4:
                return mu**4 + 6*mu**2*sigma_squared + 3*sigma_squared**2
            moment = norm(loc=mu, scale=sqrt(sigma_squared)).moment(k)
            return Rational(moment)

        if self.distribution == 'unknown':
            return sympify(f"{self.var_name}(0)^{k}")


def EV(expression):
    if issubclass(type(expression), RandomVar):
        return expression.compute_moment(1)
    else:
        return expression


def get_exponent_of(var, mono):
    monoms = mono.as_poly([var]).monoms()
    if len(monoms) > 0 and len(monoms[0]) > 0:
        return monoms[0][0]
    return 0


def get_monoms(poly: Poly):
    """
    Returns the list of monoms for a given polynomial
    """
    monoms = []
    for powers in poly.monoms():
        m = prod(var ** power for var, power in zip(poly.gens, powers))
        if m != 1:
            monoms.append(m.as_poly(poly.gens))
    return monoms


def monomial_is_constant(monomial: Poly):
    """
    Returns true iff the given monomial is constant
    """
    if monomial.is_zero:
        return True
    powers = monomial.monoms()[0]
    return all(p == 0 for p in powers)


def is_independent_from(program, v1: Symbol, v2: Symbol):
    """
    Returns true iff the two passed variables are stochastically independent
    """
    return v1 not in program.dependencies[v2]


def is_independent_from_all(program, v1: Symbol, vs: Iterable[Symbol]):
    """
    Returns true iff the first argument is stochastically independent from all variables given by the second argument
    """
    for v in vs:
        if not is_independent_from(program, v1, v):
            return False
    return True
