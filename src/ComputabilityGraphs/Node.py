from frozendict import frozendict
from .helpers import node_2_string
from .TypeSet import TypeSet


class Node(TypeSet):
    def add_passive(self,passive):
        return self.__class__(frozenset.union(self,passive))
