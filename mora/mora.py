"""This file is part of MORA

This is the main function calling the parser, the solver and then output the results
"""

from .input import InputParser, LOOP_GUARD_VAR
from .output import output_results
from .core import core
from .termination import get_expected_loop_guard_change
from timeit import default_timer as timer
from diofant.plotting import plot


def mora(source: str, goal: int = 1, output_format: str = ""):
    #try:
        start = timer()
        parser = InputParser()
        parser.set_source(source)
        program = parser.parse_source()
        invariants = core(program, goal)
        time = timer() - start

        if program.loop_guard:
            change = get_expected_loop_guard_change(invariants[LOOP_GUARD_VAR + "^1"])
            invariants[LOOP_GUARD_VAR + '_change^1'] = change

        output_results(program, invariants, time, output_format)

        if program.loop_guard:
            p1 = plot(invariants[LOOP_GUARD_VAR + "^1"], show=False, xlim=(0, None))
            #p2 = plot(invariants[LOOP_GUARD_VAR + "_change^1"], show=False)
            #p1.append(p2[0])
            p1.show()

    #except Exception as exception:
    #    print("Execution failed!")
    #    print(exception)
