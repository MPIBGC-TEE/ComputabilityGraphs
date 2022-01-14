#from .ComputerSet import ComputerSet
from typing import List, Dict, Callable
from functools import lru_cache, reduce, _lru_cache_wrapper
from inspect import signature
from copy import copy
import ComputabilityGraphs.helpers as h
import networkx as nx
from networkx.classes.function import edges

from testComputers import (
    B, C, D, E, F, G, H, 
    a_from_i,
    b_from_c_d,
    c_from_e_f,
    d_from_g_h,
)

def dep_graph(
        root_type: type,
        cs, #: Computerset,
        given: List[type] 
    ) -> nx.DiGraph:
    
    # create a graph with the computers as nodes
    # so the nodes do not need to be added  as leafs (one step less)
    
    comp_root = [c for c in cs if h.output_mvar(c) == root_type]
    if comp_root ==[]:
        return nx.DiGraph()
    else:
        css= cs.difference(given.union(comp_root))
        g = sub_graph( comp_root, css)
        return g

def sub_graph(
        comp_root: List[Callable],
        cs
    ) -> nx.DiGraph:

    g=nx.DiGraph()
    g.add_node(comp_root[0])
    
    params = [ p.annotation for p in signature(comp_root[0]).parameters.values()]

    def addsubgraph(g,param):
        gn=copy(g)
        cp = [c for c in cs if h.output_mvar(c) == param]
        if len(cp)>0:
            gn.add_edge(comp_root[0],cp[0])
            css = cs.difference(cp) 
            sg = sub_graph(cp,css)
            gn.add_edges_from(sg.edges)
            gn.add_nodes_from(sg.nodes)
        return gn

    
    res = reduce(
            addsubgraph,
            params,
            g
    )
    return res
        

def draw_matplotlib(g,ax):
    gg=nx.DiGraph()
    gg.add_edges_from(
        map(
            lambda t: (t[0].__name__,t[1].__name__)
            ,g.edges()
        )
    )
    gg.add_nodes_from(
        map(
            lambda f: f.__name__
            ,g.nodes()
        )
    )
    nx.draw_networkx(gg,ax=ax)

