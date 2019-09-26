from diofant import sympify
import re

class Update:
    # parse updates
    # takes string "x = P @ p; Q @ q" or x = RV(d, a, b)
    # creates class to deal with substituing powers of variables and moments
    # eventialy should be moved to parser
    def __init__(self, var, update_string, is_random_var=False, random_var=None):
        self.is_random_var = is_random_var
        self.random_var = random_var
        self.var = var

        # check if this is a RV or expression update
        if re.search("RV\(.+\)", update_string):
            self.is_random_var = True

            rv = re.match(r"RV\((?P<params>.+)\)", update_string)
            dist, *params = rv.group('params').split(',')# extract RV info
            dist, *params = map(str.strip, rv.group('params').split(','))
            params = list(map(sympify, params))
            self.random_var = RandomVar(dist, params)

        # here: if not is_random_var == else
        if not self.is_random_var:
            self.branches = []
            branches = update_string.split(";")
            for update in branches:
                exp, prob = update.split("@")
                self.branches.append((sympify(exp), sympify(prob)))

    def update_term(self, term, pow):
        if self.is_random_var:
            return term.subs({self.var**pow: self.random_var.compute_moment(pow) })
        else:
            return term.subs({self.var**pow: self.power(pow)})

    def power(self, k):
        return sum(prob * (exp ** k) for exp, prob in self.branches)

class RandomVar:
    def __init__(self, distribution, parameters):
        self.distribution = distribution
        self.parameters = parameters

    def compute_moment(self, k):
        if self.distribution == 'uniform':
            l, u = self.parameters
            return (u**(k+1)-l**(k+1))/((k+1)*(u-l))

## obsolete class
class UniformVar(RandomVar):
    def __init__(self, l, u):
        self.l = l
        self.u = u

    def compute_moment(self, k):
        return (self.u**(k+1)-self.l**(k+1))/((k+1)*(self.u-self.l))


#xx = Update(sympify("x"),"x + 1 @ 1/2; x+6 @ 1/2")
#print(xx.power(4))

def EV(expression):
    if issubclass(type(expression), RandomVar):
        return expression.compute_moment(1)
    else:
        return expression

def evar2init(evar):
    """returns initial value of the evariable"""
    # TODO: compute initil value
    return None
