from mora.parser import *
from mora.core import core
import sys
from timeit import default_timer as timer


def mora(input, goal=1, input_format="file", output_format=""):

    start = timer()

    prog = InputParser(input, input_format=input_format)
    if not prog.ok:
        return

    invariants = core(prog, goal=goal)

    end = timer()
    time = (end - start)

    OutputParser(prog, invariants, time, output_format=output_format)
