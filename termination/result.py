from termination.utils import Answer


class Result:
    def __init__(self):
        self.PAST = Answer.UNKNOWN
        self.AST = Answer.UNKNOWN

    def all_known(self) -> bool:
        return self.PAST.is_known() and self.AST.is_known()
