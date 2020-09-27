"""This file is part of MORA

This is the main function calling the parser, the solver and then output the results
"""

from .input import InputParser
from .output import output_results
from .core import *
from timeit import default_timer as timer


def mora(source: str, goal: int = 1, output_format: str = ""):
    try:
        print("Parsing Input")
        parser = InputParser()
        parser.set_source(source)
        program = parser.parse_source()
        print("Finished parsing")

        start = timer()
        invariants = core(program, None, goal)
        time = timer() - start
        out = output_results(program, invariants, time, output_format)
        return out
    except Exception as exception:
        print("Execution failed!")
        print(exception)
