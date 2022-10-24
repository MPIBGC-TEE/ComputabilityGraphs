from typing import Callable, Iterable
from functools import reduce
from ..dep_graph_helpers import DepGraph
from ..helpers import add_tab


class MayBeDepGraphs():
    pass


class NoDepGraphs():
    
    @ property    
    def result_set(self):
        # note: an empty set 
        # not empty graphs which would be ok
        return frozenset()    



class JustDepGraphs():
    def __init__(
        self, 
        dep_graphs: Iterable
    ):
        self.dep_graphs=dep_graphs

    
    def __eq__(self,other):
        return (
            self.__class__ == other.__class__
            and
            self.dep_graphs == other.dep_graphs
        )
    
    def __hash__(self):
        return hash(self.__class__) + hash(self.dep_graphs)
    
    def __repr__(self):
        return (
            self.__class__.__name__ + "(\n"
            + reduce(
                lambda acc,el: acc + el,
                ["\n"+add_tab(add_tab(repr(el)))+"," for el in self.dep_graphs]
            )    
            + "\n)"
        )

    @ property    
    def result_set(self):
        # decouples testing from the internal representation
        # which should become an iterator at some point
        return frozenset(self.dep_graphs)
