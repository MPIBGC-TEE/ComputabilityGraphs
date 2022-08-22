from typing import List, Set, Callable
# from copy import deepcopy
# import inspect

import networkx as nx
# from networkx.algorithms import bipartite
# from networkx.algorithms.operators.binary import difference
# from functools import lru_cache, reduce, _lru_cache_wrapper
from functools import reduce, _lru_cache_wrapper

from ComputabilityGraphs.ComputerSet import ComputerSet
from ComputabilityGraphs.helpers import (
    input_mvars,
    output_mvar,
    list_mult2
)

def add_tab(s: str):
    return "\n".join(
        [
            "\t" + line
            for line in s.split("\n")
        ]
    ) 

class OrGraph(nx.DiGraph):
    # class to represent the data structure as a bipartite networkx.DiGraph
    # which is used to draw it, (but not planned for inference)
    def draw_matplotlib(
            self,
            ax,
            computer_aliases=None,
            type_aliases=None
    ):
        pos = nx.circular_layout(self)
        # pos = nx.kamada_kawai_layout(self)
        nd = self.nodes.data()
        type_nodes = [n for n in self.nodes if nd[n]["bipartite"] == "type"]
        nx.draw_networkx_nodes(
            self, pos=pos, ax=ax, nodelist=type_nodes, node_color="blue"
        )
        computer_nodes = [
            n for n in self.nodes
            if nd[n]["bipartite"] == "computer"
        ]
        nx.draw_networkx_nodes(
            self, pos=pos, ax=ax, nodelist=computer_nodes, node_color="red"
        )
        nx.draw_networkx_edges(
            self, pos=pos, ax=ax, edgelist=self.edges()
        )

        def translate(c):
            return c.__wrapped__.__name__ if isinstance(
                c,
                _lru_cache_wrapper
            ) else c.__name__

        if computer_aliases is None:
            computer_labels = {c: translate(c) for c in computer_nodes}
        else:
            computer_labels = {
                c: computer_aliases[translate(c)] for c in computer_nodes
            }

        if type_aliases is None:
            type_labels = {t: t.__name__ for t in type_nodes}
        else:
            type_labels = {t: type_aliases[t.__name__] for t in type_nodes}

        nx.draw_networkx_labels(
            self, 
            pos=pos, 
            ax=ax, 
            labels=computer_labels, 
            font_color='black'
        )
        nx.draw_networkx_labels(
            self, 
            pos=pos, 
            ax=ax, 
            labels=type_labels, 
            font_color='white'
        )


class TypeTree:
    # superclass
    pass

class TypeNode(TypeTree):
    def __init__(
            self, 
            comp_trees: List["CompTree"] = []
    ):
        rts = set([output_mvar(ct.root_computer) for ct in comp_trees])
        if len(rts) != 1:
            raise Exception(
                "The computers of a {} have to \
                have the same result type.".format(self.__class__)
            )
        self.comp_trees = comp_trees

    def __hash__(self):
        return sum(
            [hash(ct) for ct in self.comp_trees.union({self.__class__})]
        )
    
    def __eq__(self, other):
        return self.comp_trees == other.comp_trees
    
    def __repr__(self):
        return (
            self.__class__.__name__
            + "(\n"
            + "\tcomp_trees=frozenset({"
            + reduce(
                lambda acc,el: acc + el,
                ["\n"+add_tab(add_tab(repr(el)))+"," for el in self.comp_trees]
            )    
            + "\n\t})"
            + "\n)"
        )


    @property
    def psts(self):
        # possible start types
        res = AltSet(
            frozenset.union(
                *[
                    ct.psts 
                    for ct in self.comp_trees
                ]
            )
        )
        #from IPython import embed; embed()
        return res

    @property
    def root_type(self):
        rts = [output_mvar(ct.root_computer) for ct in self.comp_trees]
        return rts[0]

    def to_OrGraph(self):
        g = OrGraph()
        root_type = self.root_type
        g.add_node(root_type, bipartite="type")
        for ct in self.comp_trees:
            g = nx.compose(g, ct.to_OrGraph())
            g.add_edge(root_type, ct.root_computer)

        return g


class TypeLeaf(TypeTree):
    def __init__(self, root_type: type):
        self.root_type = root_type

    def __hash__(self):
        return hash(self.__class__) + hash(self.root_type)

    def __repr__(self):
        return (
            self.__class__.__name__ + "("
            + self.root_type.__name__
            + ")"
        )
    def __eq__(self, other):
        return self.root_type == other.root_type
    
    @property
    def psts(self):
        #possible start types
        return AltSet([TypeSet([self.root_type])])

    def to_OrGraph(self):
        g = OrGraph()
        root_type = self.root_type
        g.add_node(root_type, bipartite="type")
        return g


class TypeSet(frozenset):
    def __str__(self):
        return (
            self.__class__.__name__
            + "({"
            + ",".join([el.__name__ for el in self])
            + "})"
        )
    def __repr__(self):
        return (
            self.__class__.__name__
            + "({"
            + ",".join([el.__name__ for el in self])
            + "})"
        )


class AltSet(frozenset):
    #def __str__(self):
    #    return (
    #        self.__class__.__name__
    #        + "({"
    #        + ",\n".join([str(el) for el in self])
    #        + "})"
    #    )
    def __repr__(self):
        return (
            self.__class__.__name__
            + "({\n\t"
            + ",\n\t".join([repr(el) for el in self])
            + "\n})"
        )


class AltSetSet(frozenset):

    #def __str__(self):
    #    return (
    #        self.__class__.__name__
    #        + "({"
    #        + ",\n".join([str(el) for el in self])
    #        + "})"
    #     )

    def __repr__(self):
        return (
            self.__class__.__name__
            + "({"
            + ",\n".join([repr(el) for el in self])
            + "})"
        )

    def combine(self) -> AltSet[TypeSet]:
        # for a computer with more than one argument the
        # altsets of the arguments have to be combined
        # The result is the set of the union of all combinations 
        # of the altsets of  the arguments.
        set_tupels = list_mult2([el for el in self])
        return AltSet([TypeSet(frozenset.union(*t)) for t in set_tupels])


class CompTree:
    def __init__(
        self,
        root_computer: Callable,
        type_trees: List[TypeTree]
    ):
        # remembering the root_computer is not strictly necessary 
        # but nice for drawing
        # We could also link upwards to it
        self.root_computer = root_computer  
        self.type_trees = type_trees
    
    def __eq__(self, other):
        return (
            (self.type_trees == other.type_trees) 
            and 
            (self.root_computer == other.root_computer)
        )

    def __hash__(self):
        return sum([
            hash(v)
            for v in (
                self.type_trees.union({
                    self.__class__, 
                    self.root_computer
                })
            )
        ])

    @property
    def psts(self) -> AltSet[TypeSet]:
        # possible start types
        # every element of sss is a set of sets
        ass = AltSetSet([tt.psts for tt in self.type_trees])
        res = ass.combine()
        return res
        
    def __repr__(self):
        return (
            self.__class__.__name__ + "(\n"
            + "\troot_computer="+self.root_computer.__name__+",\n"
            + "\ttype_trees=frozenset({"
            + reduce(
                lambda acc,el: acc + el,
                ["\n"+add_tab(add_tab(repr(el)))+"," for el in self.type_trees]
            )    
            + "\n\t})"
            + "\n)"
        )


    def to_OrGraph(self):
        g = OrGraph()
        root_computer = self.root_computer
        if self.type_trees == []:
            g.add_node(root_computer, bipartite="computer")
        else:
            g.add_node(root_computer, bipartite="computer")
            for tt in self.type_trees:
                g = nx.compose(g, tt.to_OrGraph())
                g.add_edge (root_computer, tt.root_type)
        return g


# pair of recursive functions t_tree and c_tree to generate the datastructure
# from a given target type
def t_tree(
    root_type: type,
    available_computers: ComputerSet = ComputerSet({}),
    avoid_types: Set[type] = frozenset(),
) -> TypeTree:
    def fi(c):
        return output_mvar(c)  == root_type and len(
            input_mvars(c).intersection(avoid_types)
        )==0
    
    available_result_computers = tuple(
        filter(fi, available_computers)
    )
    #from IPython import embed; embed()
    if len(available_result_computers) == 0:  # stop recursion
        return TypeLeaf(root_type) 
    else:
        return TypeNode(
            comp_trees=frozenset([
                c_tree(
                    c=c,
                    available_computers=available_computers.difference({c}),
                    avoid_types=avoid_types.union({root_type}),
                )
                for c in available_result_computers
            ]),
        )


def c_tree(
    c: Callable, available_computers: ComputerSet, avoid_types: List[type]  # computer
) -> CompTree:
    res_type = output_mvar(c)
    argset = input_mvars(c)
    return CompTree(
        root_computer=c,
        type_trees=frozenset([
            t_tree(
                root_type=v,
                available_computers=available_computers,
                avoid_types=avoid_types,
            )
            for v in argset
        ]),
    )


