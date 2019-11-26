"""This file is part of MORA

This runnable script allows the user to run MORA on probabilistic programs stored in files
For the command line arguments run the script with "--help".
"""

import glob
from argparse import ArgumentParser
from mora.mora import mora

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
        for goal in args.goals:
            mora(benchmark, goal=goal, output_format=args.output_format)


if __name__ == "__main__":
    main()
