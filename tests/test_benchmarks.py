import unittest

from diofant import symbols, simplify

from mora.core import core
from mora.utils import set_log_level, LOG_NOTHING
from mora.input import InputParser, sympify


def load_benchmark(name):
    parser = InputParser()
    parser.set_source(f"tests/benchmarks/{name}")
    return parser.parse_source()


def prepare_result(result):
    n = symbols("n")
    nint = symbols("n", integer=True)
    return sympify(result).xreplace({n: nint})


class TestBenchmarks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        set_log_level(LOG_NOTHING)

    def test_binomial_1(self):
        program = load_benchmark("binomial")
        moments = core(program, None, 1)
        x = symbols("x")

        result = prepare_result("n*p")
        self.assertEqual(simplify(moments[x] - result), 0)

    def test_binomial_2(self):
        program = load_benchmark("binomial")
        moments = core(program, None, 2)
        x = symbols("x")

        result = prepare_result("p**2*n**2 - p**2*n + p*n")
        self.assertEqual(simplify(moments[x**2] - result), 0)

    def test_binomial_3(self):
        program = load_benchmark("binomial")
        moments = core(program, None, 3)
        x = symbols("x")

        result = prepare_result("p**3*n**3 - 3*p**3*n**2 + 2*p**3*n + 3*p**2*n**2 - 3*p**2*n + p*n")
        self.assertEqual(simplify(moments[x**3] - result), 0)

    def test_cc_1(self):
        program = load_benchmark("cc")
        moments = core(program, None, 1)
        f, c, d = symbols("f,c,d")

        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[f] - result), 0)
        result = prepare_result("1 - 2**(-n)")
        self.assertEqual(simplify(moments[c] - result), 0)
        result = prepare_result("1 - 2**(-n)")
        self.assertEqual(simplify(moments[d] - result), 0)

    def test_cc_2(self):
        program = load_benchmark("cc")
        moments = core(program, None, 2)
        f, c, d = symbols("f,c,d")

        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[f**2] - result), 0)
        result = prepare_result("1 - 2**(-n)")
        self.assertEqual(simplify(moments[c**2] - result), 0)
        result = prepare_result("1 - 2**(-n)")
        self.assertEqual(simplify(moments[d**2] - result), 0)

    def test_cc_3(self):
        program = load_benchmark("cc")
        moments = core(program, None, 3)
        f, c, d = symbols("f,c,d")

        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[f**3] - result), 0)
        result = prepare_result("1 - 2**(-n)")
        self.assertEqual(simplify(moments[c**3] - result), 0)
        result = prepare_result("1 - 2**(-n)")
        self.assertEqual(simplify(moments[d**3] - result), 0)

    def test_cc4_1(self):
        program = load_benchmark("cc4")
        moments = core(program, None, 1)
        f, g, a, b, c, d = symbols("f,g,a,b,c,d")

        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[f] - result), 0)
        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[g] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[a] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[b] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[c] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[d] - result), 0)

    def test_cc4_2(self):
        program = load_benchmark("cc4")
        moments = core(program, None, 2)
        f, g, a, b, c, d = symbols("f,g,a,b,c,d")

        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[f**2] - result), 0)
        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[g**2] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[a**2] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[b**2] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[c**2] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[d**2] - result), 0)

    def test_cc4_3(self):
        program = load_benchmark("cc4")
        moments = core(program, None, 3)
        f, g, a, b, c, d = symbols("f,g,a,b,c,d")

        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[f**3] - result), 0)
        result = prepare_result("1/2")
        self.assertEqual(simplify(moments[g**3] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[a**3] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[b**3] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[c**3] - result), 0)
        result = prepare_result("-3**n*4**(-n) + 1")
        self.assertEqual(simplify(moments[d**3] - result), 0)

    def test_duelling_cowboys_1(self):
        program = load_benchmark("duelling_cowboys")
        moments = core(program, None, 1)
        ahit, bhit, y = symbols("ahit,bhit,y")

        result = prepare_result("a")
        self.assertEqual(simplify(moments[ahit] - result), 0)
        result = prepare_result("-a*b+b")
        self.assertEqual(simplify(moments[bhit] - result), 0)
        result = prepare_result("a*b - a - b")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_duelling_cowboys_2(self):
        program = load_benchmark("duelling_cowboys")
        moments = core(program, None, 2)
        ahit, bhit, y = symbols("ahit,bhit,y")

        result = prepare_result("a")
        self.assertEqual(simplify(moments[ahit**2] - result), 0)
        result = prepare_result("a**2*b - 2*a*b + b")
        self.assertEqual(simplify(moments[bhit**2] - result), 0)
        result = prepare_result("-a**2*b + a + b")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_duelling_cowboys_3(self):
        program = load_benchmark("duelling_cowboys")
        moments = core(program, None, 3)
        ahit, bhit, y = symbols("ahit,bhit,y")

        result = prepare_result("a")
        self.assertEqual(simplify(moments[ahit**3] - result), 0)
        result = prepare_result("-a**3*b + 3*a**2*b - 3*a*b + b")
        self.assertEqual(simplify(moments[bhit**3] - result), 0)
        result = prepare_result("-2*a**3*b + 6*a**2*b - 3*a*b - a - b")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_geometric_1(self):
        program = load_benchmark("geometric")
        moments = core(program, None, 1)
        x = symbols("x")

        result = prepare_result("3**(-n)*(3**n - 1)/2")
        self.assertEqual(simplify(moments[x] - result), 0)

    def test_geometric_2(self):
        program = load_benchmark("geometric")
        moments = core(program, None, 2)
        x = symbols("x")

        result = prepare_result("3**(-n)*(3**n - n - 1)")
        self.assertEqual(simplify(moments[x**2] - result), 0)

    def test_geometric_3(self):
        program = load_benchmark("geometric")
        moments = core(program, None, 3)
        x = symbols("x")

        result = prepare_result("-3**(-n)*(-11*3**n + 6*n**2 + 12*n + 11)/4")
        self.assertEqual(simplify(moments[x**3] - result), 0)

    def test_product_dep_var_1(self):
        program = load_benchmark("product_dep_var")
        moments = core(program, None, 1)
        p = symbols("p")

        result = prepare_result("n**2/4 - n/4")
        self.assertEqual(simplify(moments[p] - result), 0)

    def test_product_dep_var_2(self):
        program = load_benchmark("product_dep_var")
        moments = core(program, None, 2)
        p = symbols("p")

        result = prepare_result("n**4/16 - n**3/8 + 3*n**2/16 - n/8")
        self.assertEqual(simplify(moments[p**2] - result), 0)

    def test_product_dep_var_3(self):
        program = load_benchmark("product_dep_var")
        moments = core(program, None, 3)
        p = symbols("p")

        result = prepare_result("n**6/64 - 3*n**5/64 + 9*n**4/64 - 21*n**3/64 + 15*n**2/32 - n/4")
        self.assertEqual(simplify(moments[p**3] - result), 0)

    def test_random_walk_1d_cts_1(self):
        program = load_benchmark("random_walk_1d_cts")
        moments = core(program, None, 1)
        x = symbols("x")

        result = prepare_result("n/5")
        self.assertEqual(simplify(moments[x] - result), 0)

    def test_random_walk_1d_cts_2(self):
        program = load_benchmark("random_walk_1d_cts")
        moments = core(program, None, 2)
        x = symbols("x")

        result = prepare_result("n**2/25 + 22*n/75")
        self.assertEqual(simplify(moments[x**2] - result), 0)

    def test_random_walk_1d_cts_3(self):
        program = load_benchmark("random_walk_1d_cts")
        moments = core(program, None, 3)
        x = symbols("x")

        result = prepare_result("n**3/125 + 22*n**2/125 - 21*n/250")
        self.assertEqual(simplify(moments[x**3] - result), 0)

    def test_random_walk_2d_1(self):
        program = load_benchmark("random_walk_2d")
        moments = core(program, None, 1)
        x, y = symbols("x,y")

        result = prepare_result("0")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = prepare_result("0")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_random_walk_2d_2(self):
        program = load_benchmark("random_walk_2d")
        moments = core(program, None, 2)
        x, y = symbols("x,y")

        result = prepare_result("n/2")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = prepare_result("n/2")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_random_walk_2d_3(self):
        program = load_benchmark("random_walk_2d")
        moments = core(program, None, 3)
        x, y = symbols("x,y")

        result = prepare_result("0")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = prepare_result("0")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_running_1(self):
        program = load_benchmark("running")
        moments = core(program, None, 1)
        x, y = symbols("x,y")

        result = prepare_result("0")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = prepare_result("y(0)")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_running_2(self):
        program = load_benchmark("running")
        moments = core(program, None, 2)
        x, y = symbols("x,y")

        result = prepare_result("b**2*n/3")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = prepare_result("b**2*n**3/9 + b**2*n**2/6 + b**2*n/18 + n + y(0)**2")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_running_3(self):
        program = load_benchmark("running")
        moments = core(program, None, 3)
        x, y = symbols("x,y")

        result = prepare_result("0")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = prepare_result("b**2*n**3*y(0)/3 + b**2*n**2*y(0)/2 + b**2*n*y(0)/6 + 3*n*y(0) + y(0)**3")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_square_1(self):
        program = load_benchmark("square")
        moments = core(program, None, 1)
        x, y = symbols("x,y")

        result = prepare_result("n")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = prepare_result("n**2 + n")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_square_2(self):
        program = load_benchmark("square")
        moments = core(program, None, 2)
        x, y = symbols("x,y")

        result = prepare_result("n**2 + n")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = prepare_result("n**4 + 6*n**3 + 3*n**2 - 2*n")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_square_3(self):
        program = load_benchmark("square")
        moments = core(program, None, 3)
        x, y = symbols("x,y")

        result = prepare_result("n**3 + 3*n**2")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = prepare_result("n**6 + 15*n**5 + 45*n**4 - 15*n**3 - 30*n**2 + 16*n")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_stuttering_a_1(self):
        program = load_benchmark("stuttering_a")
        moments = core(program, None, 1)
        s = symbols("s")

        result = prepare_result("9*n/4")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_a_2(self):
        program = load_benchmark("stuttering_a")
        moments = core(program, None, 2)
        s = symbols("s")

        result = prepare_result("81*n**2/16 + n*(5*d**2/4 + 27/16)")
        self.assertEqual(simplify(moments[s**2] - result), 0)

    def test_stuttering_a_3(self):
        program = load_benchmark("stuttering_a")
        moments = core(program, None, 3)
        s = symbols("s")

        result = prepare_result("729*n**3/64 + n**2*(135*d**2/16 + 729/64) + n*(45*d**2/16 - 81/32)")
        self.assertEqual(simplify(moments[s**3] - result), 0)

    def test_stuttering_b_1(self):
        program = load_benchmark("stuttering_b")
        moments = core(program, None, 1)
        s = symbols("s")

        result = prepare_result("9*n/4")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_b_2(self):
        program = load_benchmark("stuttering_b")
        moments = core(program, None, 2)
        s = symbols("s")

        result = prepare_result("81*n**2/16 + 347*n/16 + 128/3")
        self.assertEqual(simplify(moments[s ** 2] - result), 0)

    def test_stuttering_b_3(self):
        program = load_benchmark("stuttering_b")
        moments = core(program, None, 3)
        s = symbols("s")

        result = prepare_result("729*n**3/64 + 9369*n**2/64 + 10575*n/32")
        self.assertEqual(simplify(moments[s ** 3] - result), 0)

    def test_stuttering_c_1(self):
        program = load_benchmark("stuttering_c")
        moments = core(program, None, 1)
        s = symbols("s")

        result = prepare_result("3*n**3/8 + 3*n**2/8 - n")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_c_2(self):
        program = load_benchmark("stuttering_c")
        moments = core(program, None, 2)
        s = symbols("s")

        result = prepare_result("9*n**6/64 + n**5*(3*d**2/20 + 81/160) + n**4*(d**4/24 + 7*d**2/16 - 15/32) + n**3*(d**4/9 + 3*d**2/4 - 7/8) + n**2*(d**4/8 + 11*d**2/16 + 61/64) + n*(d**4/18 + 9*d**2/40 - 1/160)")
        self.assertEqual(simplify(moments[s ** 2] - result), 0)

    def test_stuttering_c_3(self):
        program = load_benchmark("stuttering_c")
        moments = core(program, None, 3)
        s = symbols("s")

        result = prepare_result("27*n**9/512 + n**8*(27*d**2/160 + 1053/2560) + n**7*(309*d**4/2240 + 4833*d**2/4480 + 1863/8960) + n**6*(95*d**4/128 + 999*d**2/640 - 873/512) + n**5*(501*d**4/640 + 213*d**2/320 - 27/1280) + n**4*(-95*d**4/384 - 147*d**2/160 + 2241/1280) + n**3*(-579*d**4/640 - 1059*d**2/640 - 2323/2560) + n**2*(-95*d**4/192 - 519*d**2/640 - 21/256) + n*(-9*d**4/560 - 201*d**2/2240 + 3/70)")
        self.assertEqual(simplify(moments[s ** 3] - result), 0)

    def test_stuttering_d_1(self):
        program = load_benchmark("stuttering_d")
        moments = core(program, None, 1)
        s = symbols("s")

        result = prepare_result("3*n**3/8 + 3*n**2/8 - n")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_d_2(self):
        program = load_benchmark("stuttering_d")
        moments = core(program, None, 2)
        s = symbols("s")

        result = prepare_result("9*n**6/64 + 93*n**5/32 + 3091*n**4/96 + 5627*n**3/24 + 458533*n**2/576 + 8857*n/96")
        self.assertEqual(simplify(moments[s ** 2] - result), 0)

    def test_stuttering_d_3(self):
        program = load_benchmark("stuttering_d")
        moments = core(program, None, 3)
        s = symbols("s")

        result = prepare_result("27*n**9/512 + 1593*n**8/512 + 124827*n**7/1792 + 1990451*n**6/2560 + 4159077*n**5/1280 + 1144231*n**4/768 - 3081271*n**3/512 - 2634779*n**2/3840 + 8189*n/140")
        self.assertEqual(simplify(moments[s ** 3] - result), 0)

    def test_stuttering_p_1(self):
        program = load_benchmark("stuttering_p")
        moments = core(program, None, 1)
        s = symbols("s")

        result = prepare_result("3*n*p")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_stuttering_p_2(self):
        program = load_benchmark("stuttering_p")
        moments = core(program, None, 2)
        s = symbols("s")

        result = prepare_result("9*n**2*p**2 - 9*n*p**2 + 32*n*p/3")
        self.assertEqual(simplify(moments[s ** 2] - result), 0)

    def test_stuttering_p_3(self):
        program = load_benchmark("stuttering_p")
        moments = core(program, None, 3)
        s = symbols("s")

        result = prepare_result("27*n**3*p**3 - 81*n**2*p**3 + 96*n**2*p**2 + 54*n*p**3 - 96*n*p**2 + 42*n*p")
        self.assertEqual(simplify(moments[s ** 3] - result), 0)

    def test_sum_rnd_series_1(self):
        program = load_benchmark("sum_rnd_series")
        moments = core(program, None, 1)
        x, y = symbols("x,y")

        result = prepare_result("n*(n + 1)/4")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = prepare_result("n")
        self.assertEqual(simplify(moments[y] - result), 0)

    def test_sum_rnd_series_2(self):
        program = load_benchmark("sum_rnd_series")
        moments = core(program, None, 2)
        x, y = symbols("x,y")

        result = prepare_result("n*(3*n**3 + 10*n**2 + 9*n + 2)/48")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = prepare_result("n**2")
        self.assertEqual(simplify(moments[y**2] - result), 0)

    def test_sum_rnd_series_3(self):
        program = load_benchmark("sum_rnd_series")
        moments = core(program, None, 3)
        x, y = symbols("x,y")

        result = prepare_result("n**2*(n**4 + 7*n**3 + 13*n**2 + 9*n + 2)/64")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = prepare_result("n**3")
        self.assertEqual(simplify(moments[y**3] - result), 0)

    def test_init_rv_1(self):
        program = load_benchmark("test_init_rv")
        moments = core(program, None, 1)
        x, y, s = symbols("x,y,s")

        result = prepare_result("0")
        self.assertEqual(simplify(moments[x] - result), 0)
        result = prepare_result("0")
        self.assertEqual(simplify(moments[y] - result), 0)
        result = prepare_result("s(0)")
        self.assertEqual(simplify(moments[s] - result), 0)

    def test_init_rv_2(self):
        program = load_benchmark("test_init_rv")
        moments = core(program, None, 2)
        x, y, s = symbols("x,y,s")

        result = prepare_result("1/3")
        self.assertEqual(simplify(moments[x**2] - result), 0)
        result = prepare_result("1/3")
        self.assertEqual(simplify(moments[y**2] - result), 0)
        result = prepare_result("s(0)**2")
        self.assertEqual(simplify(moments[s**2] - result), 0)

    def test_init_rv_3(self):
        program = load_benchmark("test_init_rv")
        moments = core(program, None, 3)
        x, y, s = symbols("x,y,s")

        result = prepare_result("0")
        self.assertEqual(simplify(moments[x**3] - result), 0)
        result = prepare_result("0")
        self.assertEqual(simplify(moments[y**3] - result), 0)
        result = prepare_result("s(0)**3")
        self.assertEqual(simplify(moments[s**3] - result), 0)


if __name__ == '__main__':
    unittest.main()
