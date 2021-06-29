from collections.abc import Iterable
from copy import copy, deepcopy
from frozendict import frozendict
from functools import lru_cache, reduce, _lru_cache_wrapper
import inspect
from inspect import signature
from string import ascii_lowercase, ascii_uppercase
from typing import FrozenSet, Set, Callable, Tuple, List, Any
from .TypeSynonyms import Node, Decomp, ComputerSet 

def all_computer_combis_for_mvar_set(
    var_set: FrozenSet[type],
    all_computers: ComputerSet
) -> FrozenSet[ComputerSet]:
    def f(var):
        return all_computers_for_mvar(
                var,
                all_computers)

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
    allComputers: Set[Callable], available_mvars: Set[type]
) -> Set[type]:
    # fixme mm:
    # if possible replace by the new graph based method
    # We can already compute the graph. We only have to do it once and can easyly infer the union
    # of all nodes reachable from the startset.
    #
    # this is the old bottom up approach: repeatedly compute all
    # directly (in the next step) reachable Mvars and use the enriched set for
    # the next iteration until the set stays constant
    dcmvs = directly_computable_mvars(allComputers, available_mvars)

    if dcmvs.issubset(available_mvars):
        return available_mvars
    else:
        return computable_mvars(allComputers, available_mvars.union(dcmvs))


@lru_cache(maxsize=None)
def directly_computable_mvars(
    allComputers: Set[Callable], available_mvars: Set[type]
) -> Set[type]:
    # find the computers that have a source_set contained in the available_set
    return frozenset(
        [output_mvar(c) for c in applicable_computers(allComputers, available_mvars)]
    )


@lru_cache(maxsize=None)
def applicable_computers(
    allComputers: Set[Callable],
    available_mvars: Set[type]
) -> FrozenSet[Callable]:
    return frozenset(
            [
                c for c in allComputers 
                if input_mvars(c).issubset(available_mvars)
            ])

@lru_cache(maxsize=None)
def all_computers_for_mvar(
    mvar: type,
    allComputers: ComputerSet
) -> ComputerSet:
    return frozenset([c for c in allComputers if output_mvar(c) == mvar])


def arg_set(computer: Callable) -> Set[type]:
    params = signature(computer).parameters.values()
    return frozenset({param.annotation for param in params})


@lru_cache(maxsize=None)
def arg_set_set(mvar: type, allComputers: Set[Callable]) -> Set[Set[type]]:
    # return the set of arg_name_sets for all computers that
    # return this mvar
    return frozenset([arg_set(c) for c in all_computers_for_mvar(mvar, allComputers)])


@lru_cache(maxsize=None)
def all_mvars(all_computers: Set[Callable]) -> Set[type]:
    # the set of all mvars is implicitly defined by the
    # parameterlists and return values of the computers
    return reduce(
        lambda acc, c: acc.union(input_mvars(c), {output_mvar(c)}),
        all_computers,
        frozenset({}),
    )


def pretty_name(mvar: type, aliases: frozendict = frozendict({})) -> str:
    if len(aliases) == 0:
        s = mvar.__name__
        # return ((s.split('<')[1]).split('>')[0]).split('.')[-1]
    else:
        s = aliases[mvar.__name__]
    return s


# synonym for arg_set
def input_mvars(computer: Callable) -> Set[type]:
    params = signature(computer).parameters.values()
    return frozenset({param.annotation for param in params})


def output_mvar(computer: Callable) -> type:
    return signature(computer).return_annotation
