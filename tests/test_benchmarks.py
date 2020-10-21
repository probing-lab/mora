import unittest

from diofant import symbols, simplify

from mora.core import core
from mora.utils import set_log_level, LOG_NOTHING
from mora.input import InputParser, sympify


def load_benchmark(name):
    parser = InputParser()
    parser.set_source(f"tests/benchmarks/{name}")
    return parser.parse_source()


class TestBenchmarks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        set_log_level(LOG_NOTHING)

    def test_binomial_1(self):
        program = load_benchmark("binomial")
        moments = core(program, None, 1)
        x = symbols("x")

        result = sympify("n*p")
        self.assertEqual(simplify(moments[x] - result), 0)

    def test_binomial_2(self):
        program = load_benchmark("binomial")
        moments = core(program, None, 2)
        x = symbols("x")

        result = sympify("p**2*n**2 - p**2*n + p*n")
        self.assertEqual(simplify(moments[x**2] - result), 0)

    def test_binomial_3(self):
        program = load_benchmark("binomial")
        moments = core(program, None, 3)
        x = symbols("x")

        result = sympify("p**3*n**3 - 3*p**3*n**2 + 2*p**3*n + 3*p**2*n**2 - 3*p**2*n + p*n")
        self.assertEqual(simplify(moments[x**3] - result), 0)

    def test_cc_1(self):
        program = load_benchmark("cc")
        moments = core(program, None, 1)
        f, c, d = symbols("f,c,d")

        result = sympify("1/2")
        self.assertEqual(simplify(moments[f] - result), 0)
        result = sympify("1 - 2**(-n)")
        self.assertEqual(simplify(moments[c] - result), 0)
        result = sympify("1 - 2**(-n)")
        self.assertEqual(simplify(moments[d] - result), 0)

    def test_cc_2(self):
        program = load_benchmark("cc")
        moments = core(program, None, 2)
        f, c, d = symbols("f,c,d")

        result = sympify("1/2")
        self.assertEqual(simplify(moments[f**2] - result), 0)
        result = sympify("1 - 2**(-n)")
        self.assertEqual(simplify(moments[c**2] - result), 0)
        result = sympify("1 - 2**(-n)")
        self.assertEqual(simplify(moments[d**2] - result), 0)

    def test_cc_3(self):
        program = load_benchmark("cc")
        moments = core(program, None, 3)
        f, c, d = symbols("f,c,d")

        result = sympify("1/2")
        self.assertEqual(simplify(moments[f**3] - result), 0)
        result = sympify("1 - 2**(-n)")
        self.assertEqual(simplify(moments[c**3] - result), 0)
        result = sympify("1 - 2**(-n)")
        self.assertEqual(simplify(moments[d**3] - result), 0)

    def test_cc4_1(self):
        program = load_benchmark("cc4")
        moments = core(program, None, 1)
        f, g, a, b, c, d = symbols("f,g,a,b,c,d")

        result = sympify("1/2")
        self.assertEqual(simplify(moments[f] - result), 0)
        result = sympify("1/2")
        self.assertEqual(simplify(moments[g] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[a] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[b] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[c] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[d] - result), 0)

    def test_cc4_2(self):
        program = load_benchmark("cc4")
        moments = core(program, None, 2)
        f, g, a, b, c, d = symbols("f,g,a,b,c,d")

        result = sympify("1/2")
        self.assertEqual(simplify(moments[f**2] - result), 0)
        result = sympify("1/2")
        self.assertEqual(simplify(moments[g**2] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[a**2] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[b**2] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[c**2] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[d**2] - result), 0)

    def test_cc4_3(self):
        program = load_benchmark("cc4")
        moments = core(program, None, 3)
        f, g, a, b, c, d = symbols("f,g,a,b,c,d")

        result = sympify("1/2")
        self.assertEqual(simplify(moments[f**3] - result), 0)
        result = sympify("1/2")
        self.assertEqual(simplify(moments[g**3] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[a**3] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[b**3] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[c**3] - result), 0)
        result = sympify("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[d**3] - result), 0)

    def test_duelling_cowboys_1(self):
        program = load_benchmark("duelling_cowboys")
        moments = core(program, None, 1)
        ahit, bhit, y = symbols("ahit,bhit,y")

        result = sympify("a")
        self.assertEqual(simplify(moments[ahit] - result), 0)
        result = sympify("-a*b+b")
        self.assertEqual(simplify(moments[bhit] - result), 0)
        result = sympify("a*b - a - b")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_duelling_cowboys_2(self):
        program = load_benchmark("duelling_cowboys")
        moments = core(program, None, 2)
        ahit, bhit, y = symbols("ahit,bhit,y")

        result = sympify("a")
        self.assertEqual(simplify(moments[ahit**2] - result), 0)
        result = sympify("a**2*b - 2*a*b + b")
        self.assertEqual(simplify(moments[bhit**2] - result), 0)
        result = sympify("-a**2*b + a + b")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_duelling_cowboys_3(self):
        program = load_benchmark("duelling_cowboys")
        moments = core(program, None, 3)
        ahit, bhit, y = symbols("ahit,bhit,y")

        result = sympify("a")
        self.assertEqual(simplify(moments[ahit**3] - result), 0)
        result = sympify("-a**3*b + 3*a**2*b - 3*a*b + b")
        self.assertEqual(simplify(moments[bhit**3] - result), 0)
        result = sympify("-2*a**3*b + 6*a**2*b - 3*a*b - a - b")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_geometric_1(self):
        program = load_benchmark("geometric")
        moments = core(program, None, 1)
        x = symbols("x")

        result = sympify("p*(p**n - 1)/(p - 1)")
        self.assertEqual(simplify(moments[x] - result), 0)

    def test_geometric_2(self):
        program = load_benchmark("geometric")
        moments = core(program, None, 2)
        x = symbols("x")

        result = sympify("p*(p**2 + p**n*(-p**2 - 2*p + 2*p**(n + 1) - 1) + 1)/(p**3 - p**2 - p + 1)")
        self.assertEqual(simplify(moments[x**2] - result), 0)

    def test_geometric_3(self):
        program = load_benchmark("geometric")
        moments = core(program, None, 3)
        x = symbols("x")

        result = sympify("-p*(p**5 - p**3 + 5*p**2 - p**n*(p**5 + 5*p**3 + 5*p**2 + 6*p - 6*p**(n + 1) - 6*p**(n + 2) - 6*p**(n + 3) + 6*p**(2*n + 2) + 1) + 1)/(p**6 - p**5 - p**4 + p**2 + p - 1)")
        self.assertEqual(simplify(moments[x**3] - result), 0)

    def test_product_dep_var_1(self):
        program = load_benchmark("product_dep_var")
        moments = core(program, None, 1)
        p = symbols("p")

        result = sympify("n**2/4 - n/4")
        self.assertEqual(simplify(moments[p] - result), 0)

    def test_product_dep_var_2(self):
        program = load_benchmark("product_dep_var")
        moments = core(program, None, 2)
        p = symbols("p")

        result = sympify("n**4/16 - n**3/8 + 3*n**2/16 - n/8")
        self.assertEqual(simplify(moments[p**2] - result), 0)

    def test_product_dep_var_3(self):
        program = load_benchmark("product_dep_var")
        moments = core(program, None, 3)
        p = symbols("p")

        result = sympify("n**6/64 - 3*n**5/64 + 9*n**4/64 - 21*n**3/64 + 15*n**2/32 - n/4")
        self.assertEqual(simplify(moments[p**3] - result), 0)

    def test_random_walk_1d_cts_1(self):
        program = load_benchmark("random_walk_1d_cts")
        moments = core(program, None, 1)
        x = symbols("x")

        result = sympify("n/5")
        self.assertEqual(simplify(moments[x] - result), 0)

    def test_random_walk_1d_cts_2(self):
        program = load_benchmark("random_walk_1d_cts")
        moments = core(program, None, 2)
        x = symbols("x")

        result = sympify("n**2/25 + 22*n/75")
        self.assertEqual(simplify(moments[x**2] - result), 0)

    def test_random_walk_1d_cts_3(self):
        program = load_benchmark("random_walk_1d_cts")
        moments = core(program, None, 3)
        x = symbols("x")

        result = sympify("n**3/125 + 22*n**2/125 - 21*n/250")
        self.assertEqual(simplify(moments[x**3] - result), 0)

    def test_random_walk_2d_1(self):
        program = load_benchmark("random_walk_2d")
        moments = core(program, None, 1)
        x, y = symbols("x,y")

        result = sympify("0")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = sympify("0")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_random_walk_2d_2(self):
        program = load_benchmark("random_walk_2d")
        moments = core(program, None, 2)
        x, y = symbols("x,y")

        result = sympify("n/2")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = sympify("n/2")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_random_walk_2d_3(self):
        program = load_benchmark("random_walk_2d")
        moments = core(program, None, 3)
        x, y = symbols("x,y")

        result = sympify("0")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = sympify("0")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_running_1(self):
        program = load_benchmark("running")
        moments = core(program, None, 1)
        x, y = symbols("x,y")

        result = sympify("0")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = sympify("y(0)")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_running_2(self):
        program = load_benchmark("running")
        moments = core(program, None, 2)
        x, y = symbols("x,y")

        result = sympify("b**2*n/3")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = sympify("b**2*n**2/6 + b**2*n/6 + n + y(0)**2")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_running_3(self):
        program = load_benchmark("running")
        moments = core(program, None, 3)
        x, y = symbols("x,y")

        result = sympify("0")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = sympify("b**2*n**2*y(0)/2 + b**2*n*y(0)/2 + 3*n*y(0) + y(0)**3")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_square_1(self):
        program = load_benchmark("square")
        moments = core(program, None, 1)
        x, y = symbols("x,y")

        result = sympify("n")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = sympify("n**2 + n")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_square_2(self):
        program = load_benchmark("square")
        moments = core(program, None, 2)
        x, y = symbols("x,y")

        result = sympify("n**2 + n")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = sympify("n**4 + 6*n**3 + 3*n**2 - 2*n")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_square_3(self):
        program = load_benchmark("square")
        moments = core(program, None, 3)
        x, y = symbols("x,y")

        result = sympify("n**3 + 3*n**2")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = sympify("n**6 + 15*n**5 + 45*n**4 - 15*n**3 - 30*n**2 + 16*n")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_stuttering_a_1(self):
        program = load_benchmark("stuttering_a")
        moments = core(program, None, 1)
        s = symbols("s")

        result = sympify("9*n/4")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_a_2(self):
        program = load_benchmark("stuttering_a")
        moments = core(program, None, 2)
        s = symbols("s")

        result = sympify("81*n**2/16 + n*(5*d**2/4 + 27/16)")
        self.assertEqual(simplify(moments[s**2] - result), 0)

    def test_stuttering_a_3(self):
        program = load_benchmark("stuttering_a")
        moments = core(program, None, 3)
        s = symbols("s")

        result = sympify("729*n**3/64 + n**2*(135*d**2/16 + 729/64) + n*(45*d**2/16 - 81/32)")
        self.assertEqual(simplify(moments[s**3] - result), 0)

    def test_stuttering_b_1(self):
        program = load_benchmark("stuttering_b")
        moments = core(program, None, 1)
        s = symbols("s")

        result = sympify("9*n/4")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_b_2(self):
        program = load_benchmark("stuttering_b")
        moments = core(program, None, 2)
        s = symbols("s")

        result = sympify("81*n**2/16 + 347*n/16 + 128/3")
        self.assertEqual(simplify(moments[s ** 2] - result), 0)

    def test_stuttering_b_3(self):
        program = load_benchmark("stuttering_b")
        moments = core(program, None, 3)
        s = symbols("s")

        result = sympify("729*n**3/64 + 9369*n**2/64 + 10575*n/32")
        self.assertEqual(simplify(moments[s ** 3] - result), 0)

    def test_stuttering_c_1(self):
        program = load_benchmark("stuttering_c")
        moments = core(program, None, 1)
        s = symbols("s")

        result = sympify("3*n**3/8 + 3*n**2/8 - n")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_c_2(self):
        program = load_benchmark("stuttering_c")
        moments = core(program, None, 2)
        s = symbols("s")

        result = sympify("9*n**6/64 + 9*n**5/32 + n**4*(9*d**2/32 - 3/16) + n**3*(d**4/12 + 11*d**2/16 - 9/16) + n**2*(d**4/6 + 27*d**2/32 + 43/64) + n*(d**4/12 + 7*d**2/16 - 3/32)")
        self.assertEqual(simplify(moments[s ** 2] - result), 0)

    def test_stuttering_c_3(self):
        program = load_benchmark("stuttering_c")
        moments = core(program, None, 3)
        s = symbols("s")

        result = sympify("27*n**9/512 + 81*n**8/512 + n**7*(81*d**2/256 + 27/128) + n**6*(3*d**4/32 + 279*d**2/256 - 27/256) + n**5*(99*d**4/160 + 3069*d**2/1280 - 1197/2560) + n**4*(55*d**4/32 + 273*d**2/256 - 387/512) + n**3*(11*d**4/32 - 369*d**2/128 - 115/256) + n**2*(-29*d**4/16 - 69*d**2/32 + 69/64) + n*(-77*d**4/80 + 27*d**2/160 + 9/320)")
        self.assertEqual(simplify(moments[s ** 3] - result), 0)

    def test_stuttering_d_1(self):
        program = load_benchmark("stuttering_d")
        moments = core(program, None, 1)
        s = symbols("s")

        result = sympify("3*n**3/8 + 3*n**2/8 - n")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_d_2(self):
        program = load_benchmark("stuttering_d")
        moments = core(program, None, 2)
        s = symbols("s")

        result = sympify("9*n**6/64 + 9*n**5/32 + 69*n**4/16 + 2485*n**3/48 + 20875*n**2/64 + 223301*n/288")
        self.assertEqual(simplify(moments[s ** 2] - result), 0)

    def test_stuttering_d_3(self):
        program = load_benchmark("stuttering_d")
        moments = core(program, None, 3)
        s = symbols("s")

        result = sympify("27*n**9/512 + 81*n**8/512 + 675*n**7/128 + 16341*n**6/256 + 267159*n**5/512 + 1191581*n**4/512 + 835053*n**3/256 - 441649*n**2/192 - 947777*n/192")
        self.assertEqual(simplify(moments[s ** 3] - result), 0)

    def test_stuttering_p_1(self):
        program = load_benchmark("stuttering_p")
        moments = core(program, None, 1)
        s = symbols("s")

        result = sympify("3*n*p")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_p_2(self):
        program = load_benchmark("stuttering_p")
        moments = core(program, None, 2)
        s = symbols("s")

        result = sympify("9*n**2*p**2 - 9*n*p**2 + 32*n*p/3")
        self.assertEqual(simplify(moments[s ** 2] - result), 0)

    def test_stuttering_p_3(self):
        program = load_benchmark("stuttering_p")
        moments = core(program, None, 3)
        s = symbols("s")

        result = sympify("27*n**3*p**3 - 81*n**2*p**3 + 96*n**2*p**2 + 54*n*p**3 - 96*n*p**2 + 42*n*p")
        self.assertEqual(simplify(moments[s ** 3] - result), 0)

    def test_sum_rnd_series_1(self):
        program = load_benchmark("sum_rnd_series")
        moments = core(program, None, 1)
        x, y = symbols("x,y")

        result = sympify("n*(n + 1)/4")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = sympify("n")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_sum_rnd_series_2(self):
        program = load_benchmark("sum_rnd_series")
        moments = core(program, None, 2)
        x, y = symbols("x,y")

        result = sympify("n*(3*n**3 + 10*n**2 + 9*n + 2)/48")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = sympify("n**2")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_sum_rnd_series_3(self):
        program = load_benchmark("sum_rnd_series")
        moments = core(program, None, 3)
        x, y = symbols("x,y")

        result = sympify("n**2*(n**4 + 7*n**3 + 13*n**2 + 9*n + 2)/64")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = sympify("n**3")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_init_rv_1(self):
        program = load_benchmark("test_init_rv")
        moments = core(program, None, 1)
        x, y, s = symbols("x,y,s")

        result = sympify("0")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = sympify("0")
        self.assertEqual(simplify(moments[y] - result), 0)
        result = sympify("s(0)")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_init_rv_2(self):
        program = load_benchmark("test_init_rv")
        moments = core(program, None, 2)
        x, y, s = symbols("x,y,s")

        result = sympify("1/3")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = sympify("1/3")
        self.assertEqual(simplify(moments[y**2] - result), 0)
        result = sympify("s(0)**2")
        self.assertEqual(simplify(moments[s**2] - result), 0)

    def test_init_rv_3(self):
        program = load_benchmark("test_init_rv")
        moments = core(program, None, 3)
        x, y, s = symbols("x,y,s")

        result = sympify("0")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = sympify("0")
        self.assertEqual(simplify(moments[y**3] - result), 0)
        result = sympify("s(0)**3")
        self.assertEqual(simplify(moments[s**3] - result), 0)


if __name__ == '__main__':
    unittest.main()
