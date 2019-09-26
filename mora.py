
from parser import InputParser, OutputParser
from core import core
from benchmarks import *

prog = InputParser(example1)

invariants = core(prog, goal=3)

OutputParser(invariants)
