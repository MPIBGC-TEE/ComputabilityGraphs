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

from .TypeSynonyms import Node, Decomp, Computer, ComputerSet
from . import helpers as h

def add_Node(
        g: nx.DiGraph,
        s: Node
) -> nx.DiGraph:

    G = deepcopy(g)
    G.add_node(s, bipartite=0)
    return G

def add_Decomp(
        g: nx.DiGraph,
        s: Decomp
) -> nx.DiGraph:

    G = deepcopy(g)
    G.add_node(s, bipartite=1)
    return G


def add_combi_arg_set_graph(
        g: nx.DiGraph,
        decomp: Decomp,
        computer_combi: Set[Computer]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:
    _, passive = decomp
    args = reduce(frozenset.union,[h.arg_set(computer) for computer in computer_combi],frozenset())
    arg_node = frozenset.union(args,passive)
    e = (arg_node, decomp)
    # A situation arising from combis like {a(c),b(d)} and {b(c),a(d)}
    G = deepcopy(g)
    if G.has_edge(*e):
        key = 'computer_sets'
        data = G.get_edge_data(*e)[key]
        G.get_edge_data(*e)[key] =frozenset.union(data,frozenset({computer_combi}))
        return (G, frozenset())
    else:
        G = add_Node(g, arg_node)
        # if edge does not exist
        G.add_edge(arg_node, decomp, computer_sets=frozenset([computer_combi]))
        return (G, frozenset({arg_node}))


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


def add_all_arg_set_graphs_to_decomp(
        g: nx.DiGraph,
        decomp: Decomp,
        all_computers
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:  
    g_new = deepcopy(g)
    active, passive = decomp
    all_combies = h.all_computer_combis_for_mvar_set(active,all_computers)
    # we want to add only nodes that are not supersets of other nodes (we are
    # interested in a SPARSE graph) but if a computercombi creates a new egde
    # to an EXISTING node we want to add the edge and therefore have to include
    # the combi in the call to add_combis_arg_set_graphs_to_decomp

    def src2node(ss):
        return frozenset.union(ss, passive)

    src_sets = frozenset(map(h.combi_arg_set, all_combies))
    src_sets_wo_ss = h.remove_supersets(src_sets)
    src_nodes_wo_ss = frozenset(map(src2node, src_sets_wo_ss))
    super_sets = frozenset.difference(src_sets, src_sets_wo_ss)
    super_set_nodes = frozenset(map(src2node, super_sets))
    super_set_nodes_already_in_g = frozenset.intersection(
        frozenset(g_new),
        super_set_nodes
    )

    relevant_nodes = frozenset.union(
        super_set_nodes_already_in_g,
        src_nodes_wo_ss
    )
    relevant_combis = frozenset(
        filter(
            lambda combi: src2node(h.combi_arg_set(combi)) in relevant_nodes,
            all_combies
        )
    )

    return add_combis_arg_set_graphs_to_decomp(
                g_new,
                decomp,
                relevant_combis
            )


def add_arg_set_graphs_to_decomps(
        g: nx.DiGraph,
        decomps: Set[Decomp],
        all_computers: FrozenSet[Computer]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:
    def f(acc, el):
        pp('el',locals())
        g, new_nodes = acc
        decomp = el
        active, passive = decomp
        g_new, combi_new_nodes = add_all_arg_set_graphs_to_decomp(g, decomp, all_computers)
        pp('combi_new_nodes',locals())

        new_nodes = frozenset.union(new_nodes, combi_new_nodes)
        return(g_new, new_nodes)

    return reduce(f, decomps, (g, frozenset()))

def add_all_decompositions_to_node(
        g: nx.DiGraph,
        node: Node,
        uncomputable: FrozenSet[type]
    ) -> Tuple[nx.DiGraph, FrozenSet[Decomp]]:
    actives = h.power_set(node)
    decompositions = [
        (a,frozenset.difference(node,a)) 
        for a in actives 
        if len(frozenset.intersection(a, uncomputable)) == 0 
    ]
    new_decompositions = frozenset(filter(lambda d: not(g.has_node(d)), decompositions))
    for d in decompositions:
        g = add_Decomp(g, d)
        g.add_edge(d,node)

    return (g, new_decompositions)

def fast_graph(cs: ComputerSet) -> nx.DiGraph:    
    # The iterator has not been implemented yet
    # this is a manual version
    g, new_dcs = initial_fast_graph(cs)
    g_new, arg_set_nodes = add_arg_set_graphs_to_decomps(g ,new_dcs, cs)
    
    uncomputable = h.uncomputable(cs)
    def f(acc, node):
        g, decompositions = acc
        g_new, node_decomps = add_all_decompositions_to_node(g, node, uncomputable=uncomputable)
        new_decompositions = frozenset.union(
            decompositions,
            node_decomps
        )
        return g_new, new_decompositions

    g_new2, new_dcs2 = reduce(f, arg_set_nodes, (g_new, frozenset()))
    g_new3, arg_set_nodes = add_arg_set_graphs_to_decomps(g_new2 ,new_dcs2, cs)

    return g_new3


def initial_fast_graph(cs: ComputerSet) -> nx.DiGraph:    
    g = nx.DiGraph()
    mvs = h.all_mvars(cs)
    for v in mvs:
        g = add_Node(g, frozenset([v]))

    computables = frozenset.difference(mvs,  h.uncomputable(cs))
    new_decompositions = frozenset(
        [
            (frozenset([v]), frozenset([])) 
            for v in computables
        ]
    )
    for dn in new_decompositions:
        g = add_Decomp(g, dn) 
        g.add_edge(dn,dn[0])

    return g, new_decompositions 
    
