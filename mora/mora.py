"""This file is part of MORA

This is the main function calling the parser, the solver and then output the results
"""

from .input import InputParser, LOOP_CONDITION_VAR
from .output import output_results
from .core import core
from .termination import get_expected_loop_condition_change
from timeit import default_timer as timer


def mora(source: str, goal: int = 1, output_format: str = ""):
    try:
        start = timer()
        parser = InputParser()
        parser.set_source(source)
        program = parser.parse_source()
        invariants = core(program, goal)
        time = timer() - start

        if program.loop_condition:
            expected_delta = get_expected_loop_condition_change(invariants[LOOP_CONDITION_VAR + "^1"])
            invariants['loop_delta^1'] = expected_delta

        output_results(program, invariants, time, output_format)

    except Exception as exception:
        print("Execution failed!")
        print(exception)
