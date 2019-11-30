from diofant import sympify, Rational
from scipy.stats import norm
from math import sqrt
import re


class Update:
    # parse updates
    # takes string "x = P @ p; Q @ q" or x = RV(d, a, b)
    # creates class to deal with substituting powers of variables and moments
    def __init__(self, var, update_string, is_random_var=False, random_var=None):
        self.is_random_var = is_random_var
        self.update_string = update_string
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
                self.branches.append((sympify(exp), sympify(prob)))
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
        if self.distribution == 'uniform':
            l, u = self.parameters
            return (u**(k+1)-l**(k+1))/((k+1)*(u-l))

        if self.distribution == 'gauss' or self.distribution == 'normal':
            mu, sigma_squared = self.parameters
            moment = norm(loc=mu, scale=sqrt(sigma_squared)).moment(k)
            return Rational(moment)

        if self.distribution == 'unknown':
            return f"{self.var_name}(0)^{k}"


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
