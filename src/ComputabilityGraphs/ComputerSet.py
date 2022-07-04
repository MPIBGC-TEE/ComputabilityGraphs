from . str_helpers import compset_2_string

class ComputerSet(frozenset):
    def __str__(self):
        return compset_2_string(self)
