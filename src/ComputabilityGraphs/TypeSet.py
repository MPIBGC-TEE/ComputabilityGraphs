from frozendict import frozendict
from .str_helpers import node_2_string

class TypeSet(frozenset):
    def __str__(
            self,
            aliases=frozendict()
        ):
        return node_2_string(self,aliases)
