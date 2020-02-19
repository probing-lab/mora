"""
This module implements the simple rule that checks whether the loop terminates immediately
because of the initial condition
"""
from diofant import sympify

from termination.rule import Rule, Result


class InitialStateRule(Rule):
    def is_applicable(self):
        return True

    def run(self):
        loop_guard = sympify(self.program.loop_guard)
        for var, update in self.program.initial_values.items():
            if hasattr(update, "branches"):
                loop_guard = loop_guard.subs({var: update.branches[0][0]})

        is_loop_guard = not loop_guard.is_number or bool(loop_guard > 0)

        return Result.UNKNOWN if is_loop_guard else Result.PAST
