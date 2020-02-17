"""
This module contains implementations common to all termination proof rules
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from diofant import Expr
from mora.core import Program


class Result(Enum):
    PAST = auto()
    AST = auto()
    NONTERM = auto()
    UNKNOWN = auto()


class Rule(ABC):

    def __init__(self, loop_guard_change: Expr, martingale_expression: Expr, program: Program):
        self.loop_guard_change = loop_guard_change
        self.martingale_expression = martingale_expression
        self.program = program

    @abstractmethod
    def is_applicable(self) -> bool: pass

    @abstractmethod
    def run(self) -> Result: pass
