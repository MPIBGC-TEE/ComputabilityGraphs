from . import helpers as h

class ComputerSetSet(frozenset):
    def __str__(self):
        return "{" + ",".join([str(cs) for cs in self]) + "}"
