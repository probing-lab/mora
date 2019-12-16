
from random import random


def run_program():
    n = 0
    x = 0
    y = 0
    while x + 1 > 0:
        n += 1
        y = y + 1
        if random() < 2/3:
            x = x + 2*y**3
        else:
            x = x - 10*y**2
        if n % 100 == 0:
            print(f'x = {x}')

    return n


n = run_program()
print(n)
