"""This file is part of MORA

This runnable script allows the user to run MORA on probabilistic programs stored in files
For the command line arguments run the script with "--help".
"""

import glob
from argparse import ArgumentParser

from mora.input import InputParser
from mora.mora import mora
from termination import decide_termination

parser = ArgumentParser(description="Run MORA on probabilistic programs stored in files")

parser.add_argument(
    "--benchmarks",
    dest="benchmarks",
    required=True,
    type=str,
    nargs="+",
    help="A list of benchmarks to run MORA on"
)

parser.add_argument(
    "--goals",
    dest="goals",
    type=int,
    nargs="+",
    default=[1, 2, 3],
    help="A list of moments MORA should consider"
)

parser.add_argument(
    "--termination",
    dest="termination",
    default=False,
    action="store_true",
    help="If set, the termination behavior of the benchmarks are investigated. Also, 'goals' gets ignored if this "
         "flag is set "
)

parser.add_argument(
    "--bounds",
    dest="bounds",
    default=False,
    action="store_true",
    help="This is just a development flag. If set, it calculates the asymptotic bounds of the program variables"
)

parser.add_argument(
    "--output_format",
    dest="output_format",
    type=str,
    choices=["text", "latex"],
    default="text",
    help="The format in which MORA should present the output"
)


def main():
    args = parser.parse_args()
    args.benchmarks = [b for bs in map(glob.glob, args.benchmarks) for b in bs]

    for benchmark in args.benchmarks:
        if args.termination:
            program = mora(benchmark, goal=1, output_format=args.output_format)
            decide_termination(program)
        elif args.bounds:
            ip = InputParser()
            ip.set_source(benchmark)
            program = ip.parse_source()
            print(program)
        else:
            for goal in args.goals:
                mora(benchmark, goal=goal, output_format=args.output_format)


if __name__ == "__main__":
    main()
