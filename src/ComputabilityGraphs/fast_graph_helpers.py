from functools import lru_cache, reduce
import networkx as nx
import time
import matplotlib.pyplot as plt
from matplotlib.colors import CSS4_COLORS, BASE_COLORS, TABLEAU_COLORS
from pygraphviz.agraph import AGraph
from typing import List, Set, Tuple, Callable, FrozenSet
from copy import deepcopy
from frozendict import frozendict
from testinfrastructure.helpers import pp, pe

from .non_graph_helpers import (
    # computable_mvars
    # ,directly_computable_mvars
    #input_mvars
    ## ,output_mvar
    #,
    arg_set
    ## ,arg_set_set
    #,
    #all_mvars
    ## ,applicable_computers
    #,
    #all_computers_for_mvar,
    #pretty_name,
)

def add_set(
        g: nx.DiGraph,
        s: FrozenSet[type]
) -> nx.DiGraph:
    
    G = deepcopy(g)
    G.add_node(s,bipartite=0)
    return G

def add_combi_arg_set_graph(
        g: nx.DiGraph,
        decomp: Tuple[Set[type]],
        computer_combi:Set[Callable[[Tuple[type]],type]]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[type]
]:
    def f(
        arg_set: Set[type],
        new_args: Set[type]
    ) -> FrozenSet[type]:
        c = deepcopy(set(arg_set))
        c.union(new_args)
        return frozenset(c)

    args = reduce(f,[arg_set(computer) for computer in computer_combi],frozenset())
    e = (args,decomp)
    
    #A situation arising from combis like {a(c),b(d)} and {b(c),a(d)}    
    G = deepcopy(g)
    if G.has_edge(*e): 
        data = G.get_edge_data(*e)
        old = data["computer_sets"]
        new = merge_sets(old,combi)
        data = new
        return (G,frozenset())
    else:
        G = add_set(g, args)
        # if edge does not exist
        G.add_edge(args, decomp, computer_sets=frozenset([computer_combi]))
        return (G, args)
