from frozendict import frozendict
from .TypeSet import TypeSet


class Node(TypeSet):
    def add_passive(self,passive):
        return self.__class__(frozenset.union(self,passive))
