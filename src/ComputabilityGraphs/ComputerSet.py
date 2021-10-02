from . import helpers as h

class ComputerSet(frozenset):
    def __str__(self):
        return h.compset_2_string(self)
