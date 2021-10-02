#from typing import NamedTuple
from frozendict import frozendict
from collections import namedtuple
from .helpers import varsettuple_2_string
from .Node import Node

_decomposition = namedtuple('Decomposition',['active','passive'])
class Decomposition(_decomposition):
    def __str__(
            self,
            aliases=frozendict()
        ):
        return varsettuple_2_string(self,aliases)

    def add_passive(self,passive):
        return self.__class__(
                active=self.active,
                passive=self.passive.add_passive(passive)
        )
