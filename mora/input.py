"""This file is part of MORA

This file contains the parser which parses source-files containing prob-solvable loops and
converts them into a format which can be further used by the program.
"""

from diofant import symbols, Symbol
from .utils import *
from .core import Program
import os
from lark import Lark, Visitor

GRAMMAR_FILE_PATH = "mora/prob_solvable.lark"


class InputParser:
    def __init__(self):
        self.__program = Program()

    def set_source(self, source: str):
        if os.path.isfile(source):
            with open(source) as file:
                self.__program.source = file.read()
                self.__program.name = source.split("/")[-1]
        else:
            # Temporary modification to allow string input to MORA instead of from a file.
            self.__program.source = source
            self.__program.name = "from_text"
            #raise Exception(f"File {source} not found")

    def parse_source(self):
        with open(GRAMMAR_FILE_PATH) as grammar_file:
            lark_parser = Lark(grammar_file)

        tree = lark_parser.parse(self.__program.source)
        visitor = UpdateProgramVisitor(self.__program)
        visitor.visit(tree)
        self.__set_unknown_initializations()
        self.__set_finite_value_rvs()
        self.__set_dependencies()
        return self.__program

    def __set_finite_value_rvs(self):
        program_variables = set(self.__program.variables)
        for variable, update in self.__program.updates.items():
            if update.is_random_var is False:
                all_branches_constant = True
                for branch, _ in update.branches:
                    if branch.free_symbols & program_variables:
                        all_branches_constant = False
                        break
                if all_branches_constant:
                    update.is_random_var = True
                    update.random_var = RandomVar("finite", update.branches)

    def __set_dependencies(self):
        ancestors = self.__program.ancestors
        variables = self.__program.variables
        for variable in variables:
            dependencies = {v for v in variables if ancestors[variable] & ancestors[v]}
            self.__program.dependencies[variable] = dependencies

    def __set_unknown_initializations(self):
        for v in self.__program.variables:
            if v not in self.__program.initial_values.keys():
                self.__program.initial_values[v] = Update(v, "RV(unknown)")


class UpdateProgramVisitor(Visitor):
    def __init__(self, program: Program):
        self.program = program
        self.forbidden_variables = set()

    def initialization(self, tree):
        variable = symbols(str(tree.children[0]))
        expression = str(tree.children[1])
        self.program.initial_values[variable] = Update(variable, expression)

    def update(self, tree):
        variable = symbols(str(tree.children[0]))
        if variable in self.forbidden_variables:
            raise Exception("Program is not prob-solvable. Circular variable dependencies.")
        expression = str(tree.children[1])
        self.program.variables.append(variable)
        self.program.updates[variable] = Update(variable, expression, program_variables=self.program.variables)
        self.forbidden_variables.union(
            self.program.updates[variable].update_term(variable, 1).free_symbols
        ).difference(self.program.variables)
        self.__set_ancestors_for_variable(variable)

    def __set_ancestors_for_variable(self, variable: Symbol):
        if self.program.updates[variable].is_random_var:
            self.program.ancestors[variable] = set()
            return

        parents = set()
        for branch in self.program.updates[variable].branches:
            parents = parents.union(branch[0].free_symbols)
        parents = parents.intersection(self.program.variables)

        ancestors = parents.copy()
        for parent in parents:
            if parent != variable:
                ancestors = ancestors.union(self.program.ancestors[parent])

        self.program.ancestors[variable] = ancestors
