"""This file is part of MORA

This runnable script allows the user to run MORA on probabilistic programs stored in files
For the command line arguments run the script with "--help".
"""

import glob
from argparse import ArgumentParser

from mora.mora import mora
from termination import decide_termination
from termination.bounds import bounds


HEADER = """
  _____           _  _______                  _             _             
 |  __ \         | ||__   __|                (_)           | |            
 | |__) | __ ___ | |__ | | ___ _ __ _ __ ___  _ _ __   __ _| |_ ___  _ __ 
 |  ___/ '__/ _ \| '_ \| |/ _ \ '__| '_ ` _ \| | '_ \ / _` | __/ _ \| '__|
 | |   | | | (_) | |_) | |  __/ |  | | | | | | | | | | (_| | || (_) | |   
 |_|   |_|  \___/|_.__/|_|\___|_|  |_| |_| |_|_|_| |_|\__,_|\__\___/|_|   
"""


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
    type=str,
    default="",
    help="This is just a development flag. If set, it calculates the asymptotic bounds of the given expression"
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
            print(HEADER)
            program = mora(benchmark, goal=1, output_format=args.output_format)
            decide_termination(program)
        elif args.bounds:
            bounds(benchmark, args.bounds)
        else:
            for goal in args.goals:
                mora(benchmark, goal=goal, output_format=args.output_format)


if __name__ == "__main__":
    main()
