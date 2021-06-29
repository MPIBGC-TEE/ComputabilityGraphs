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

from .helpers import (
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
    ,
    all_computers_for_mvar,
    # pretty_name,
)

from .TypeSynonyms import Node, Decomp, Computer, ComputerSet 
# Type synonyms
#Node = FrozenSet[type]
#Decomp = Tuple[Node]
#Computer = Callable[[Tuple[type]], type]
#ComputerSet = FrozenSet[Computer]


def add_Node(
        g: nx.DiGraph,
        s: Node
) -> nx.DiGraph:

    G = deepcopy(g)
    G.add_node(s, bipartite=0)
    return G

def all_computer_combis_for_node(
    node: Node,
    all_computers, ComputerSet
) -> FrozenSet[ComputerSet]:
    mcs = map(all_computers_for_mvar,node) 
    

def add_combi_arg_set_graph(
        g: nx.DiGraph,
        decomp: Decomp,
        computer_combi: Set[Computer]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:
    args = reduce(frozenset.union,[arg_set(computer) for computer in computer_combi],frozenset())
    e = (args, decomp)
    # A situation arising from combis like {a(c),b(d)} and {b(c),a(d)}
    G = deepcopy(g)
    if G.has_edge(*e):
        key = 'computer_sets'
        data = G.get_edge_data(*e)[key]
        G.get_edge_data(*e)[key] =frozenset.union(data,frozenset({computer_combi}))
        return (G, frozenset())
    else:
        G = add_Node(g, args)
        # if edge does not exist
        G.add_edge(args, decomp, computer_sets=frozenset([computer_combi]))
        return (G, frozenset({args}))


def add_combis_arg_set_graphs_to_decomp(
        g: nx.DiGraph,
        decomp: Decomp,
        computer_combis: FrozenSet[ComputerSet]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:
    def f(acc, el):
        g, new_nodes = acc
        computer_combi = el
        g_new,combi_new_nodes = add_combi_arg_set_graph(g, decomp, computer_combi)
        new_nodes = frozenset.union(new_nodes, combi_new_nodes)
        return(g_new, new_nodes)

    return reduce(f, computer_combis, (g, frozenset()))

def add_arg_set_graphs_to_decomp(
        g: nx.DiGraph,
        decomp: Decomp,
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:
    active, passive = decomp
    all_computer_combies(active,all_computers)
    return all_combis_arg_set_graphs_to_decomp(
                g,
                decomp,
                all_computer_combies
            )

       

def add_arg_set_graphs_to_decomps(
        g: nx.DiGraph,
        decomps: Set[Decomp],
        allcomputers: FrozenSet[Computer]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:
    def f(acc, el):
        g, new_nodes = acc
        decomp = el
        active, passive = decomp
        all_computer_combies(active,all_computers)
        g_new, add_combis_arg = add_combis_arg_set_graph_to_decomp(g, decomp, computer_combis)
        new_nodes = frozenset.union(new_nodes, combi_new_nodes)
        return(g_new, new_nodes)

    return reduce(f, computer_combis, (g, frozenset()))

