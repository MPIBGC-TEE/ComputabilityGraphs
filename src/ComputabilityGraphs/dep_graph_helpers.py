#from .ComputerSet import ComputerSet
from typing import List, Dict, Callable
from functools import lru_cache, reduce, _lru_cache_wrapper
from inspect import signature
from copy import copy
import ComputabilityGraphs.helpers as h
import networkx as nx
from networkx.classes.function import edges

class DepGraph(nx.DiGraph):
    def __eq__(self, other):
        return (
            self.nodes == other.nodes and
            self.edges == other.edges
        )


    def draw_matplotlib(self,ax):
        gg=nx.DiGraph()
        gg.add_edges_from(
            map(
                lambda t: (t[0].__name__,t[1].__name__)
                ,self.edges()
            )
        )
        gg.add_nodes_from(
            map(
                lambda f: f.__name__
                ,self.nodes()
            )
        )
        nx.draw_networkx(gg,ax=ax,pos=nx.kamada_kawai_layout(gg))


    def required_mvars(self):
        leaf_comps = [n for n in self.nodes if self.out_degree(n) == 0]
        return reduce(
                lambda acc,comp: acc.union(h.input_mvars(comp)),
                leaf_comps,
                frozenset({})
        )
    

    def __hash__(self):
        return hash(
            (
                frozenset(self.nodes()),
                frozenset(self.edges())
            )
        )


def dep_graph(
        root_type: type,
        cs, #: Computerset,
        given: List[type] 
    ) -> DepGraph:
    
    # create a graph with the computers as nodes
    # so the nodes do not need to be added  as leafs (one step less)
    
    comp_root = tuple([c for c in cs if h.output_mvar(c) == root_type])
    if len(comp_root) == 0:
        return DepGraph()
    else:
        css= cs.difference(given.union(comp_root))
        g = sub_graph( comp_root, css)
        return g


@lru_cache
def sub_graph(
        comp_root: List[Callable],
        cs
    ) -> DepGraph:

    g=DepGraph()
    root_computer=comp_root[0]
    g.add_node(root_computer)
    
    params = tuple([ p.annotation for p in signature(root_computer).parameters.values()])

    def addsubgraph(g,param):
        gn=copy(g)
        cp = tuple([c for c in cs if h.output_mvar(c) == param])
        if len(cp)>0:
            param_computer = cp[0]
            gn.add_edge(root_computer, param_computer)
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
        


def computer_list_for_mvar(mvar, all_computers):
    return [ comp for comp in all_computers if h.output_mvar(comp) == mvar ] 


def computer_combies(cs,given):
    # dependency graphs in the sense of this module  only work if there
    # is only one possibility to compute a given variable.
    # If there is a variable with more than one computer yielding it,
    # we get alternative dep graphs.
    # We can compute a variable if one of the dep graphs is computable 
    # with the given values.
    # This function finds all the given  unique computersets.

    
    comp_lists = [computer_list_for_mvar(var,cs) for  var in h.all_output_types(cs).difference(given)]
    return h.list_mult(comp_lists)
    
def all_dep_graphs(root_type,cs,given):
    return map(
            lambda combi:dep_graph(root_type,frozenset(combi),given),
            computer_combies(cs,given)
    )


def computable_dep_graphs(root_type,cs,given):
    res = filter(
        lambda g: g.required_mvars().issubset(given),
        all_dep_graphs(root_type,cs,given)
    )
    #from IPython import embed; embed()
    return res


def shortest_computable_dep_graph(root_type,cs,given):
    cgs=tuple(computable_dep_graphs(root_type,cs,given))
    if len(cgs)>0: 
        return sorted(
            computable_dep_graphs(
                root_type,
                cs,
                given
            ),
            key=lambda g: len(g.edges)
        )[0] 
    else:
        raise Exception("This variable can not computed from the given values")


def computer_dict(cs):
    return {var: computer_list_for_mvar(var,cs) for  var in h.all_output_types(cs)}


def duplicated_computer_dict(cs):
    cd=computer_dict(cs)
    return { k:v for k,v in cd.items() if len(v)>1}
