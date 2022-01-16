from collections.abc import Iterable
from copy import copy, deepcopy
from frozendict import frozendict
from functools import lru_cache, reduce, _lru_cache_wrapper
import inspect
from inspect import signature
from string import ascii_lowercase, ascii_uppercase
from typing import FrozenSet, Set, Callable, Tuple, List, Any

from networkx.algorithms.operators.binary import union
from .TypeSynonyms import  Computer
from .ComputerSet import ComputerSet
from .Node import Node
from .TypeSet import TypeSet
from .str_helpers import node_2_string

def all_computer_combis_for_mvar_set(
    var_set: FrozenSet[type],
    all_computers: ComputerSet,
    avoid_nodes: FrozenSet[Node] = frozenset()
) -> FrozenSet[ComputerSet]:
    def f(var):
        return all_computers_for_mvar(
            var,
            all_computers,
            avoid_nodes
        )

    comp_lists = [list(s) for s in map(f,var_set)]
    comp_tuple_list = list_mult(comp_lists)
    return frozenset([frozenset(t) for t in comp_tuple_list])


def list_mult(
    ll: Tuple[List]
    ) ->  List[Tuple]:
    def totup(x):
        t= tuple(x) if isinstance(x,Iterable) else (x,)
        return t
    return tuple_list_mult([ [totup(el) for el in l] for l in ll])


def tuple_list_mult(
    ll: Tuple[List[Tuple]]
) -> List[Tuple]:
    if len(ll) == 0:
        return tuple()
    if len(ll) == 1:
        return ll[0]
    if len(ll) >= 1:
        new_last = [t2+t1 for t1 in ll[-1] for t2 in ll[-2]]
        return tuple_list_mult(ll[0:-2]+[new_last])

def module_computers(cmod):
    #sep = "."
    #pkg_name = __name__.split(sep)[0]
    #cmod = importlib.import_module(".resolve.computers", package=pkg_name)
    def pred(a):
        return inspect.isfunction(a) or isinstance(a,_lru_cache_wrapper)
    return frozenset(
        [
            getattr(cmod, c)
            for c in cmod.__dir__()
            if pred(getattr(cmod, c))
        ]
    )


def module_computer_aliases(cmod):
    comp_abbreviations = list_mult([ascii_lowercase for i in range(2)])
    return frozendict({
        v.__name__: comp_abbreviations[i]
        for i, v in enumerate(module_computers(cmod))
    })


def module_mvar_aliases(cmod):
    var_abbreviations = list_mult([ascii_uppercase for i in range(2)])
    allVars = all_mvars(module_computers(cmod))
    return frozendict({
        name: var_abbreviations[i]
        for i, name in enumerate(sorted(map(lambda v: v.__name__, allVars)))
    })

def merge_dicts(d1, d2):
    e = copy(dict(d1))
    e.update(d2)
    return frozendict(e)

@lru_cache(maxsize=None)
def computable_mvars(
    allComputers: FrozenSet[Callable], available_mvars: FrozenSet[type]
) -> FrozenSet[type]:
    # fixme mm:
    dcmvs = directly_computable_mvars(allComputers, available_mvars)
    print(node_2_string(dcmvs))

    if dcmvs.issubset(available_mvars):
        return available_mvars
    else:
        return computable_mvars(allComputers, available_mvars.union(dcmvs))


@lru_cache(maxsize=None)
def directly_computable_mvars(
    allComputers: FrozenSet[Callable], available_mvars: FrozenSet[type]
) -> FrozenSet[type]:
    # find the computers that have a source_set contained in the available_set
    return frozenset(
        [
            output_mvar(c)
            for c in applicable_computers(allComputers, available_mvars)
        ]
    )


@lru_cache(maxsize=None)
def applicable_computers(
    allComputers: FrozenSet[Callable],
    available_mvars: FrozenSet[type]
) -> FrozenSet[Callable]:
    return frozenset(
            [
                c for c in allComputers
                if input_mvars(c).issubset(available_mvars)
            ])


@lru_cache(maxsize=None)
def all_computers_for_mvar(
    mvar: type,
    allComputers: ComputerSet,
    avoid_nodes: FrozenSet[Node] = frozenset()
) -> ComputerSet:
    return frozenset(
        [
            c for c in allComputers 
            if output_mvar(c) == mvar and not any(
                [ 
                    frozenset.issuperset(
                        input_mvars(c),
                        an
                    )
                    for an in avoid_nodes
                ]

            ) 
        ]
    )


def arg_set(computer: Callable) -> FrozenSet[type]:
    params = signature(computer).parameters.values()
    return frozenset({param.annotation for param in params})



def combi_arg_set(
        combi: FrozenSet[Computer]
        ) -> FrozenSet[type]:
    def f(acc, el):
        return frozenset.union(acc, arg_set(el))

    return reduce(f,combi,frozenset())


@lru_cache(maxsize=None)
def arg_set_set(mvar: type, allComputers: FrozenSet[Callable]) -> FrozenSet[Set[type]]:
    # return the set of arg_name_sets for all computers that
    # return this mvar
    return frozenset([arg_set(c) for c in all_computers_for_mvar(mvar, allComputers)])


@lru_cache(maxsize=None)
def all_mvars(all_computers: FrozenSet[Callable]) -> FrozenSet[type]:
    # fixme mm 11-04-2021:
    # rename to all_types

    # the set of all mvars is implicitly defined by the
    # parameterlists and return values of the computers
    return all_output_types(all_computers).union(
            all_input_types(all_computers)
    )


def all_output_types(all_computers: FrozenSet[Callable]) -> FrozenSet[type]:
    return reduce(
        lambda acc, c: acc.union({output_mvar(c)}),
        all_computers,
        frozenset({})
    )

def all_input_types(all_computers: FrozenSet[Callable]) -> FrozenSet[type]:
    return reduce(
        lambda acc, c: acc.union(input_mvars(c)),
        all_computers,
        frozenset({})
    )

# synonym for arg_set
def input_mvars(computer: Callable) -> FrozenSet[type]:
    params = signature(computer).parameters.values()
    return frozenset({param.annotation for param in params})


def output_mvar(computer: Callable) -> type:
    return signature(computer).return_annotation


def remove_supersets(ss: FrozenSet[FrozenSet])->FrozenSet[FrozenSet]:
    sl = sorted(list(ss), key=len)  # smallest sets first
    checked,to_do = remove_supersets_from_sorted_list([],sl)
    return frozenset(checked)

def remove_supersets_from_sorted_list(
        checked: List[FrozenSet],
        to_do: List[FrozenSet]
) -> List[FrozenSet]:
    if len(to_do) == 0 :
        return (checked,[])
    else:
        fst = to_do[0]
        rest = list(filter(lambda s : not(s.issuperset(fst)),to_do[1:]))
        return remove_supersets_from_sorted_list(checked + [fst], rest)

def uncomputable(cs: ComputerSet) -> FrozenSet[type]:
    all_res = frozenset([output_mvar(c) for c in cs])
    all_vars = all_mvars(cs)
    return frozenset.difference(all_vars,all_res)

def sublist_without_pos(s,pos):
    sl1=slice(0,pos)
    sl2=slice(pos+1,None)
    return s[sl1] + s[sl2]

def power_set(s):
    ls = list(s)
    if len(ls)==0:
        l = []
    else: 
        l = [[]] + power_list(ls) 
    return frozenset(map(frozenset,l))

def power_list(s):
    if len(s)==0:
        raise
    if len(s) == 1:
        return [s]
    if len(s) >1:
        sublists = [sublist_without_pos(s,ind) for ind in range(len(s))] 
        psls = [power_list(sl) for sl in  sublists]
        return reduce( lambda acc,el:acc + el, psls) + [s]

###################################################
# common graph helpers

import networkx as nx
def equivalent_singlegraphs(g1_single: nx.DiGraph, g2_single: nx.DiGraph) -> bool:
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
