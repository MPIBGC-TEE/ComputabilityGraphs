import networkx as nx
import inspect
from typing import Dict, List, Set, Callable

from functools import lru_cache
from frozendict import frozendict
from copy import deepcopy
from copy import copy
from functools import reduce
import matplotlib.pyplot as plt

from . import helpers as h
from .str_helpers import nodes_2_string
from .graph_helpers import minimal_startnodes_for_single_var
from .ComputerSet import ComputerSet
from . import fast_graph_helpers as fgh
from . import rec_graph_helpers as rgh
from . import dep_graph_helpers as dgh
from ComputabilityGraphs.or_graph_helpers import (
    t_tree,
    TypeSet,
    AltSet
)

# choose which implementation to use
# at the moment rgh is much faster
# graph_maker = fgh.fast_graph
graph_maker = rgh.fast_graph


class CMTVS:
    """CMTVS stands for
    (C)onnected(M)ulti(T)ype(V)alue(S)et and is a set of
    values that all have different type It is immutable
    and supports normal set operations (inherited from
    frozenset) for its variables.
    The (C)onnection is established by a set of functions with
    explicit type signature.
    The type  signatures are used to build dependency graphs for
    every type of variable, to determine, values of which type
    have to be added to the set if a certain result (type) is
    desired.
    The functions themselfs are used to compute these results
    if the dependencies are present in the set and to predict
    computable types.
    For computable values methods are automatically added
    to the instace of an CMTVS."""

    # This class is explicitly instantiated (even in the model source.py) from an  iterable.
    # The models source.py becomes A (as opposed to THE) way to create a MVarSet instance
    # which can also be created arbitrarily (and programmatically) somewhere else.
    # Not all MVarSets of interest are "Models" some are "ModelRuns" (=Simulations including a Model but extending it with known parameterizations, startvalues)
    # The models submodule of bgc_md2 is just a convienience to assemble MVarSets that
    # express models.
    # Actually in the case of Williams the MvarSet expresses a ModelRun with
    # units (which motivates a possible second submodule modelruns
    # that will contain modelruns which will refer to a particular model and
    # just add parameterizations and start values)

    def update(self, other: Set[type]):
        """Although an instance of this class is a set, every variable in the set has a unique type. This is very similar to a dictionary where the keys are unique.
        Accordingly CMTVS objects have an update method like a dictionay. There are however two differences:
        1.  While the update method of a dictionary takes
            a dictionary as an argument, this mehtod takes
            an iterable and uses the types of the elements
            implicitly as keys.
        2.  While the update mehtod of a dictionary changes
            the object in place, this method returns a copy
            and leaves the object unchanged.
        """

        new = deepcopy(self)
        new._fd = frozendict({**self._fd, **{type(el): el for el in other}})
        return new

    def __init__(
            self,
            iterable,
            computers
        ):
        self._fd = frozendict({type(el): el for el in iterable})
        self.computers = frozenset(computers)

    def jupyter_widget(
            self,
            root_type: type,
            type_aliases_tup=None,
            computer_aliases_tup=None
        ):

        if type_aliases_tup is None:
            type_aliases_tup = h.numbered_aliases(
                "T",
                h.all_mvars(self.computers)
            )

        if computer_aliases_tup is None:
            computer_aliases_tup = h.numbered_aliases(
                "f",
                self.computers
            )

        og = t_tree(
            root_type=root_type,
            available_computers=self.computers,
            avoid_types=frozenset({}),
            given_types=self.provided_mvar_types
        )
        return og.jupyter_widget(
            computer_aliases_tup=computer_aliases_tup,
            type_aliases_tup=type_aliases_tup,
            given=self.provided_mvar_types
        )

    @property
    def provided_mvar_values(self):
        return frozenset([i for i in self._fd.values()])

    @property
    def provided_mvar_types(self) -> Set[type]:
        return frozenset(type(v) for v in self.provided_mvar_values)

    def computable_mvar_types(self) -> Set[type]:
        return h.computable_mvars(
            allComputers=self.computers, available_mvars=self.provided_mvar_types
        )

    def __dir__(self):
        return super().__dir__() + [
            "get_{}".format(t.__name__) for t in self.computable_mvar_types()
        ]

    def __repr__(self):
        el_str = ", ".join([k.__name__ + " = " + str(v) for k, v in self._fd.items()])
        return self.__class__.__name__ + "({" + el_str + "})"

    def __getattribute__(self, name):
        if name.startswith("get_"):
            var_name = name[4:]
            # for var in self.mvars:
            for var in self.computable_mvar_types():
                if var.__name__ == var_name:
                    #return lambda: self._get_single_value(var)
                    return lambda: self._get_single_value_by_TypeTree(var)
        return super().__getattribute__(name)

    # @lru_cache(maxsize=None)
    def path_dict_to_single_mvar(self, t: type) -> Dict[type, List[Set[type]]]:
        node = frozenset({t})
        spsg = fgh.project_to_multiDiGraph(
            graph_maker(root_type=t, cs=self.computers, given=self.provided_mvar_types)
        )
        graph_min_nodes = minimal_startnodes_for_single_var(spsg, t)
        pmvs = self.provided_mvar_types

        model_min_nodes = list(filter(lambda n: n.issubset(pmvs), graph_min_nodes))
        if len(model_min_nodes) < 1:
            raise (
                Exception(
                    "The desired t can not be computed from the provided mvars:"
                    + node_2_string(pmvs)
                    + "Minimal sets to compute it are"
                    + nodes_2_string(graph_min_nodes)
                )
            )

        path_dict = frozendict(
            {
                n: list(nx.all_shortest_paths(spsg, source=n, target=node))
                for n in model_min_nodes
            }
        )
        return path_dict

    def _get_single_value(self, t: type, path: List[Set[type]] = []):  # ->t:
        # fixme mm 03-07-2020:
        # This is interesting: The function actually returns
        # an instance of class t, I do not know yet how to express that with
        # the static type hint system.
        # (Obviously the return type  is a function of the input types)

        pvs = self.provided_mvar_values
        pv_dict = {type(v): v for v in pvs}
        # print(pv_dict)
        if t in [type(v) for v in pvs]:
            return pv_dict[t]

        path_dict = self.path_dict_to_single_mvar(t)
        start_nodes = path_dict.keys()

        if path == []:
            default_start_node = sorted(start_nodes, key=lambda node: len(node))[0]
            path = path_dict[default_start_node][0]
        else:
            # check if the given path is among the possible paths
            start_node = path[0]
            if start_node not in path_dict.keys():
                raise (
                    Exception("There are no paths to the target with this startnode")
                )
            starting_here = path_dict[start_node]
            if not path in starting_here:
                raise (Exception("the given path is not possible"))

        # create results step by step along the graph
        spsg = fgh.project_to_multiDiGraph(
            graph_maker(root_type=t, cs=self.computers, given=self.provided_mvar_types)
        )
        rg = spsg.subgraph(path).copy()
        rg.nodes[path[0]]["values"] = pvs
        for i in range(1, len(path)):
            computers = rg.get_edge_data(path[i - 1], path[i])[0][
                "computers"
            ]  # [0] if we have more than one computerset take the first one

            def apply(comp):
                arg_classes = [
                    p.annotation for p in inspect.signature(comp).parameters.values()
                ]
                arg_values = [pv_dict[cl] for cl in arg_classes]
                res = comp(*arg_values)
                return res

            pv_dict.update({h.output_mvar(c): apply(c) for c in computers})

        return pv_dict[t]

    def _get_single_value_by_depgraph(
        self,
        t: type,
    ):  # ->t:

        pvs = self.provided_mvar_values
        pv_dict = {type(v): v for v in pvs}
        # print(pv_dict)
        if t in [type(v) for v in pvs]:
            return pv_dict[t]

        # create results step by step along the graph
        g = dgh.shortest_computable_dep_graph(
            root_type=t, cs=self.computers, given=self.provided_mvar_types
        )

        return g.compute_value(t, pvs) 


    def _get_single_value_by_TypeTree(
        self,
        t: type,
    ):  # ->t:

        pvs = self.provided_mvar_values
        pv_dict = {type(v): v for v in pvs}
        # print(pv_dict)
        pvt = TypeSet({type(v) for v in pvs})
        if t in pvt:
            return pv_dict[t]
        # create the or_graph datastructure
        type_tree = t_tree(
            root_type=t,
            available_computers=self.computers,
            given_types=pvt
        )
        # find the computable depgraphs
        dgs = type_tree.computable_depgraphs(pvt).result_set
        # the result is an iterable.
        # So it has an __iter__ method  which returns the iterator
        itr = dgs.__iter__()
        # we only need the first element (this enables us to implement  the
        # method computable_depgraphs later in a lazy way. (not as a  set or
        # list)
        dg = next(itr)

        # from IPython import embed; embed()
        # og = type_tree.to_networkx_graph(pvt)
        # fig = plt.figure(figsize=(20,20))
        # ax = fig.add_subplot(1, 1, 1)
        # og.draw_matplotlib(ax)
        # fig.savefig("OrGraphNX.pdf")

        return dg.compute_value(t, pvs) 
