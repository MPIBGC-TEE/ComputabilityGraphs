from frozendict import frozendict
#from .str_helpers import node_2_string

#class TypeSet(frozenset):
#    def __str__(
#            self,
#            aliases=frozendict()
#        ):
#        return node_2_string(self,aliases)

class TypeSet(frozenset):
    def __str__(self):
        return (
            self.__class__.__name__
            + "({})".format(self.short_str()) 
        )

    def short_str(self):
        return (
            "{"
            + ",".join([el.__name__ for el in self])
            + "}"
        )
    def __repr__(self):
        return (
            self.__class__.__name__
            + "({"
            + ",".join([el.__name__ for el in self])
            + "})"
        )

