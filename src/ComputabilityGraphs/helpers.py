from string import ascii_lowercase, ascii_uppercase
from frozendict import frozendict
from functools import _lru_cache_wrapper
import inspect
#from . import computers as cmod
from . import non_graph_helpers as ngh
from copy import copy

def list_mult(ll):
    # tensor product of list....
    if len(ll) == 0:
        return []
    if len(ll) == 1:
        return ll[0]
    if len(ll) == 2:
        l1 = ll[-1]
        l2 = ll[-2]
        new_last = [t2+t1 for t1 in l1 for t2 in l2]
        return new_last

    return list_mult(ll[0:-2]+[new_last])


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
    allVars = ngh.all_mvars(module_computers(cmod))
    return frozendict({
        name: var_abbreviations[i]
        for i, name in enumerate(sorted(map(lambda v: v.__name__, allVars)))
    })

def merge_dicts(d1, d2):
    e = copy(dict(d1))
    e.update(d2)
    return frozendict(e)

def merge_sets(s1, s2):
    s = copy(set(s1))
    s.union(s2)
    return frozenset(s)
