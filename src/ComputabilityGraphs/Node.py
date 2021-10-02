from frozendict import frozendict
from .helpers import node_2_string


class Node(frozenset):
    def __str__(
            self,
            aliases=frozendict()
        ):
        return node_2_string(self,aliases)

    def add_passive(self,passive):
        return self.__class__(frozenset.union(self,passive))
