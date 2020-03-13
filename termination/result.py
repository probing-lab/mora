from termination.utils import Answer


class Result:

    def __init__(self):
        self.PAST = Answer.UNKNOWN
        self.AST = Answer.UNKNOWN
        self.witnesses = []

    def all_known(self) -> bool:
        return self.PAST.is_known() and self.AST.is_known()

    def add_witness(self, witness):
        self.witnesses.append(witness)

    def print(self):
        print()
        print()
        print("PAST: ", self.PAST)
        print(" AST: ", self.AST)
        print()
        print()
        for witness in self.witnesses:
            witness.print()
            print()
            print()