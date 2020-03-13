"""
This module contains implementations common to all termination proof rules
"""

from abc import ABC, abstractmethod
from diofant import Expr
from mora.core import Program
from termination.result import Result


class Rule(ABC):

    def __init__(self, loop_guard_change: Expr, martingale_expression: Expr, program: Program):
        self.loop_guard_change = loop_guard_change
        self.martingale_expression = martingale_expression
        self.program = program

    @abstractmethod
    def is_applicable(self) -> bool: pass

    @abstractmethod
    def run(self, result: Result) -> Result: pass


class Witness(ABC):

    def __init__(self, kind):
        self.kind = kind
        self.data = {}
        self.explanation = ""

    def print(self):
        headline = f"Witness for {self.kind}"
        print(headline)
        print("".join(["-" for n in range(len(headline))]))
        key_length = max([len(k) for k in self.data.keys()]) + 2

        for key, value in self.data.items():
            print(f"{key.ljust(key_length)} {value}")

        print()
        print("Explanation:")
        print(self.explanation)
