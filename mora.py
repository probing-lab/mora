"""
TO DO:
'!!!' - cruitial functionality
'!'   - need for evaluation
''    - nice to have/additional features/readability
parameters:
    !!!- extract/parse # and add to polynomial domain for computation

input parser:
    - __repr__  methods for nicer representation

solver"
    - recursive->stack
    !- return rather than print (&have output parser to print/outfile/tex/etc)
    - helper fxs->utils & utils Update class->parser

core:
    - not exact [?]

mora:
    !- input args from command (sys.args)
    !- timer total [& vs just solving recs]

distributions:
    - create separate file to have various supported distributions, e.g.
      uniform, gauss, binomial, etc

unit testing:
    - yep

readme:
    - input
    - output
    - add own rnd dist
    - run all evaluation (reproduce results)fv
"""
from parser import InputParser, OutputParser
from core import core

prog = InputParser("""x = 0
while true:
    u = RV(uniform, 0, d)
    x = x + u @ 1
    y = y + x - 2*u @ 1""")

invariants = core(prog, goal=["y"])

OutputParser(invariants)





example1 = """x = 0
while true:
    u = RV(uniform, 0, d)
    x = x + u @ 1
    y = y + x - 2*u @ 1"""
