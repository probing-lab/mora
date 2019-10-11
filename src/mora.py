
from parser import InputParser, OutputParser
from core import core
import sys



def mora(input, goal=1, input_format="file", output_format="tex"):

    prog = InputParser(input, input_format=input_format)

    invariants = core(prog, goal=goal)

    OutputParser(prog, invariants, output_format=output_format)

    
if len(sys.argv)>2:
    input = sys.argv[1]
    goal = sys.argv[2:]
    mora(input, goal=goal, input_format="file", output_format="tex")
