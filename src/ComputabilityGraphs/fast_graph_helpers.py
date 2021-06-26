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
    # input_mvars
    # ,output_mvar
    # ,
    arg_set
    # ,arg_set_set
    # ,
    # all_mvars
    # ,applicable_computers
    # ,
    # all_computers_for_mvar,
    # pretty_name,
)


def add_set(
        g: nx.DiGraph,
        s: FrozenSet[type]
) -> nx.DiGraph:

    G = deepcopy(g)
    G.add_node(s, bipartite=0)
    return G


def add_combi_arg_set_graph(
        g: nx.DiGraph,
        decomp: Tuple[Set[type]],
        computer_combi:Set[Callable[[Tuple[type]],type]]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[type]
]:
    args = reduce(frozenset.union,[arg_set(computer) for computer in computer_combi],frozenset())
    e = (args, decomp)
    #A situation arising from combis like {a(c),b(d)} and {b(c),a(d)}    
    G = deepcopy(g)
    if G.has_edge(*e): 
        key = 'computer_sets'
        data = G.get_edge_data(*e)[key]
        G.get_edge_data(*e)[key] =frozenset.union(data,frozenset({computer_combi}))
        return (G, frozenset())
    else:
        G = add_set(g, args)
        # if edge does not exist
        G.add_edge(args, decomp, computer_sets=frozenset([computer_combi]))
        return (G, frozenset({args}))


def add_combis_arg_set_graphs(
        g: nx.DiGraph,
        decomp: Tuple[Set[type]],
        computer_combis:FrozenSet[FrozenSet[Callable[[Tuple[type]],type]]]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[FrozenSet[type]]
]:
    def f(acc,el):
        g,new_nodes = acc
        computer_combi = el
        g_new,combi_new_nodes = add_combi_arg_set_graph(g,decomp,computer_combi)
        new_nodes=frozenset.union(new_nodes,combi_new_nodes)
        return(g_new,new_nodes)
    return reduce(f,computer_combis,(g,frozenset()))
            
