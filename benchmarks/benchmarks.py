test = """
x = 0
while true:
    u = RV(gauss, 0, 1)
    x = x + u
    y = y + u
    z = (y-x)^2
    """

cc = """
f = 0
c = 0
d = 0
while true:
   f = 1 @ 1/2; 0 @ 1/2
   c = 1 - f + c*f @ 1
   d = d + f - d*f @ 1
"""

cc4 = """
f = 0
g = 0
a = 0
b = 0
c = 0
d = 0
while true:
   f = 1 @ 1/2; 0 @ 1/2
   g = 1 @ 1/2; 0 @ 1/2
   a = a + (1-a)*f*g @ 1
   b = b + (1-b)*f*(1-g) @ 1
   c = c + (1-c)*(1-f)*g @ 1
   d = d + (1-d)*(1-f)*(1-g) @ 1
"""

random_walk_1d_cts = """
v = 0
x = 0
while true:
    v = RV(uniform, 0, 1)
    x = x + v @ 7/10; x - v @ 3/10
"""

sum_rnd_series = """
n = 0
x = 0
while true:
    n = n + 1 @ 1
    x = x + n @ 1/2; x @ 1/2
"""

product_dep_var = """f = 0
x = 0
y = 0
p = 0
while true:
    f = 0 @ 1/2; 1 @ 1/2
    x = x + f @ 1
    y = y + 1 - f @ 1
    p = x*y @ 1"""

random_walk_2d = """
h = 0
x = 0
y = 0
while true:
    h = 1 @ 1/2; 0 @ 1/2
    x = x-h @ 1/2; x + h @ 1/2
    y = y+(1-h) @ 1/2; y-(1-h) @ 1/2
"""

binomial = """
x = 0
while true:
    x = x + 1 @ p; x @ 1-p
"""

introA = """
v = 0
w = 0
f = 0
x = -1
y = 1
s = 0
while true:
   v = RV(uniform,1-d,1+d)
   w = RV(uniform,2-2*d,2+2*d)
   f = 1 @ 3/4; 0 @ 1/4
   x = x + f*v
   y = y + f*w @ 1
   s = x + y @ 1
"""

introC = """
v = 0
w = 0
f = 0
x = -1
y = 1
s = 0
while true:
   v = RV(uniform, 1-d, 1+d)
   w = RV(uniform, 2-2*d, 2+2*d)
   f = 1 @ 3/4; 0 @ 1/4
   x = x + f*v @ 1
   y = y + f*w @ 1
   s = s + x*y @ 1
"""

square = """
x = 0
y = 1
while true:
    x = x+2 @ 1/2; x @ 1/2
    y = x^2 @ 1
"""

#??? not same as before. unsure which result is correct.
introP = """
f = 0
x = -1
y = 1
s = 0
while true:
    u1 = RV(uniform, 0, 2)
    u2 = RV(uniform, 0, 4)
    f = 1 @ p; 0 @ 1-p
    x = x + f*u1 @ 1
    y = y + f*u2 @ 1
    s = x + y @ 1
"""

# Programs below this have not been checked

test_init_rv = """
x = RV(uniform, -1, 1)
y = RV(uniform, -1, 1)
while true:
    x = x
    y = y
    s = s
"""

#??? not same as before. unsure which result is correct.
introB = """
v = 0
w = 0
x = RV(uniform, -9, 7)
y = RV(uniform, -7, 9)
s = 0
f = 0
while true:
    v = RV(uniform, -3, 5)
    w = RV(uniform, -6, 10)
    f = 1 @ 3/4; 0
    x = x + f*v
    y = y + f*w
    s = x + y
"""

introD = """
v = 0
w = 0
x = RV(uniform, -9, 7)
y = RV(uniform, -7, 9)
s = 0
f = 0
while true:
    v = RV(gauss, 1, 16/3)
    w = RV(uniform, -6, 10)
    f = 1 @ 3/4; 0
    x = x + f*v
    y = y + f*w
    s = s + x*y
"""

geometric = """
x = 0
c = 1
while true:
    c = c @ p; 0 @ 1-p
    x = x + c @ 1
"""

test2 = """
x = 0
y = 1
z = 2
while true:
    x = x+2 @ 1/2; x
    y = x^2 @ 1/3; x^2 + 3*x + 9
    z = 2*z @ 1/5; z + y + x
"""
