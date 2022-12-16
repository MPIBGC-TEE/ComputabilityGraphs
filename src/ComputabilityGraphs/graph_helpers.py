from functools import reduce
import networkx as nx
import time
from typing import Set, Callable
# from copy import deepcopy
from frozendict import frozendict
# from testinfrastructure.helpers import pp, pe

from .helpers import (
    all_mvars
)

from .fast_graph_helpers import fast_graph, project_to_multiDiGraph, combine
from .FastGraph import FastGraph

#a decorator to time the execution of some of the graph building functions
def mm_timeit(f):
    def timed(*args,**kw):
        ts = time.time()
        result = f(*args,**kw)
        te = time.time()
        print("func:"+str(f.__name__)+": "+str(te-ts))
        return result

    return timed


def immutable_edge(edge):
    s, d, dat = edge
    return (s, d, frozendict(dat))


@mm_timeit
def equivalent_multigraphs(
    g1_multi: nx.MultiDiGraph,
    g2_multi: nx.MultiDiGraph
) -> bool:
    # since we deal with a multigraph
    # it is possible to get several edges between two nodes.
    # The method get_edge_data returns a dictionary
    # with the numbers of these edges as keys.
    # But we want to consider two graphs equivalent if the resulting
    # SET is equal, in other words:
    # If a graph has two edges EACH from : A->B
    # we do not care which of the edges has which computerset
    # Therefore we compare the set of computersets belonging

    g1_single = toDiGraph(g1_multi)
    g2_single = toDiGraph(g2_multi)
    return all(
        [
            g1_single.get_edge_data(*e) == g2_single.get_edge_data(*e)
            for e in g1_single.edges()
        ]
        + [
            g1_single.get_edge_data(*e) == g2_single.get_edge_data(*e)
            for e in g2_single.edges()
        ]
    ) & (g1_single.nodes() == g2_single.nodes())



def fast_sparse_powerset_graph(
        computers
    ):
    def f(g,root_type):
        fg = fast_graph(
         root_type,
         computers
        )
        g=deepcopy(g)
        return combine(g,fg)

    mvars=all_mvars(computers)
    sgs = [
            fast_graph(root_type,computers) 
            for root_type in mvars
    ]

    cfg = reduce(f,mvars,FastGraph())
    return project_to_multiDiGraph(cfg)


def update_generator(
        computers: Set[Callable],
        max_it: int
    ) -> 'iterator':

    if max_it < 0:
        raise IndexError("update sequence indices have to be larger than 0")

    val = initial_sparse_powerset_graph(computers)
    yield val
    old = deepcopy(val)
    val = update_step(val, computers)

    # print(equivalent_multigraphs(old, val))

    counter = 1
    while max_it > counter and not (equivalent_multigraphs(old, val)):
        yield val
        old = deepcopy(val)
        val = update_step(val, computers)
        counter += 1
        # print("counter", counter, "equivalent?", equivalent_multigraphs(old, val))


def toDiGraph(g_multi: nx.MultiDiGraph) -> nx.DiGraph:
    def edgeDict_to_set(ed):
        target = "computers"
        comp_set_set = frozenset([
            v[target]
            for v in ed.values() if target in v.keys()
        ])
        return comp_set_set

    g_single = nx.DiGraph()
    for e in g_multi.edges():
        s, t = e
        edgeDict = g_multi.get_edge_data(s, t)
        comp_set_set = edgeDict_to_set(edgeDict)
        if g_single.has_edge(s, t):
            comp_set_set = comp_set_set.union(
                g_single.get_edge_data(s, t)["computers"]
            )
        g_single.add_edge(s, t, computers=comp_set_set)
    return g_single


def minimal_startnodes_for_single_var(spg: nx.Graph, targetVar: type):
    """ spg is a sparse powerset Graph, which means that it only contains all one element sets as targets."""
    # We first create a graph with the direction of the edges reversed
    rev_spg = spg.reverse(copy=True)
    targetSet = frozenset({targetVar})
    res = nx.single_source_shortest_path(rev_spg, source=targetSet)
    # res=nx.shortest_path(spg,target=targetSet)
    possible_startnodes = frozenset(res.keys())
    minimal_startnodes = [
        n for n in filter(lambda n: not (n.issuperset(targetSet)), possible_startnodes)
    ]
    return frozenset(minimal_startnodes)


def minimal_target_subgraph_for_single_var(spg: nx.Graph, targetVar: type):
    # all minimal starting points
    targetNode = frozenset({targetVar})
    start_nodes = minimal_startnodes_for_single_var(spg, targetVar)
    path_list_list = [
        nx.shortest_path(spg, target=targetNode, source=sn) for sn in start_nodes
    ]
    connected_nodes = reduce(
        lambda acc, pl: acc.union(pl), path_list_list, frozenset({})
    )
    return spg.subgraph(connected_nodes).copy()


def minimal_startnodes_for_node(spg: nx.Graph, targetNode: Set[type]) -> Set[Set]:
    if spg.has_node(targetNode):
        # The targetNode is already part of the spg.
        # (because it has been added in one of the update
        # steps as an argument set of a computer)
        # in which case we can simply return the startnodes
        # of the paths leading to it.
        path_dict = nx.shortest_path(spg, target=targetNode)
        possible_startnodes = frozenset(path_dict.keys())
    else:
        # Although we do not find the node itself
        # we can find the nodes for the single element sets
        # of the mvars in the node, since we have built the graph
        # starting wiht them. E.g if node {A,B,C} is not part of
        # the graph we know at least that the nodes {A}, {B} amd {C}
        # are in the graph.
        # For each of them we can compute the subgraph of
        # spg that leads to it. If we compute the product of these
        # subgraphs it will contain the desired node.

        # fixme: mm 02-26-2020
        # We could make this more efficient by looking for all the
        # disjoint unions of the targetNode Mvars and compute
        # the product of the graphs leading to the subsets.
        # If the subsets are not one element sets we need fewer
        # multiplications.
        # prod_g=product_graph(*[target_subgraph(spg,frozenset({v})) for v in targetNode])
        prod_g = product_graph(
            *[minimal_target_subgraph_for_single_var(spg, v) for v in targetNode]
        )
        prod_path_dict = nx.shortest_path(prod_g, target=targetNode)
        possible_startnodes = frozenset(prod_path_dict.keys())

    def filter_func(n):
        # remove every set that contains one of the variables we are looking for ...
        return not (any([(v in n) for v in targetNode]))

    minimal_startnodes = frozenset(
        [n for n in filter(filter_func, possible_startnodes)]
    )
    return minimal_startnodes
