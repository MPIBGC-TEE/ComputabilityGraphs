from typing import List, Set, Callable

# from copy import deepcopy
# import inspect

import networkx as nx

# from networkx.algorithms import bipartite
# from networkx.algorithms.operators.binary import difference
# from functools import lru_cache, reduce, _lru_cache_wrapper
from functools import reduce, _lru_cache_wrapper
import matplotlib.pyplot as plt
from collections import OrderedDict
import igraph as ig
from ipywidgets import Layout, Button, Box, VBox, Label, HTMLMath, Output

from .OrGraphs.MayBeDepGraphs import NoDepGraphs, JustDepGraphs, MayBeDepGraphs
from .dep_graph_helpers import DepGraph

from ComputabilityGraphs.ComputerSet import ComputerSet
from .TypeSet import TypeSet
from .helpers import input_mvars, output_mvar, list_mult2, add_tab


class AltSet(frozenset):
    # def __str__(self):
    #    return (
    #        self.__class__.__name__
    #        + "({"
    #        + ",\n".join([str(el) for el in self])
    #        + "})"
    #    )
    def __repr__(self):
        return (
            self.__class__.__name__
            + "({\n\t"
            + ",\n\t".join([repr(el) for el in self])
            + "\n})"
        )


class AltSetSet(frozenset):

    # def __str__(self):
    #    return (
    #        self.__class__.__name__
    #        + "({"
    #        + ",\n".join([str(el) for el in self])
    #        + "})"
    #     )-vals_array_mean[0])

    def __repr__(self):
        return (
            self.__class__.__name__
            + "({"
            + ",\n".join([repr(el) for el in self])
            + "})"
        )

    def combine(self) -> "AltSet[TypeSet]":
        # for a computer with more than one argument the
        # altsets of the arguments have to be combined
        # The result is the set of the union of all combinations
        # of the altsets of  the arguments.
        set_tupels = list_mult2([el for el in self])
        return AltSet([TypeSet(frozenset.union(*t)) for t in set_tupels])


def add_tab(s: str):
    return "\n".join(["\t" + line for line in s.split("\n")])


def type_node_to_str(n, type_aliases, avoid_nodes_visible=True):
    # from IPython import embed; embed()
    t, avoid_types = n
    if avoid_nodes_visible:
        res = (
            "{}\n{}".format(t.__name__, TypeSet(avoid_types).short_str())
            if type_aliases is None
            else "{}\n{}".format(
                type_aliases[t],
                ("{" + ",".join([type_aliases[t] for t in avoid_types]) + "}"),
            )
        )

    else:
        res = (
            "{}".format(t.__name__)
            if type_aliases is None
            else "{}".format(type_aliases[t])
        )

    return res


def computer_node_to_str(n, computer_aliases):
    c, avoid_types = n
    if computer_aliases is None:
        res = (
            c.__wrapped__.__name__ if isinstance(c, _lru_cache_wrapper) else c.__name__
        )
    else:
        res = computer_aliases[c]
    return res


class OrGraphNX(nx.DiGraph):
    # class to represent the data structure as a bipartite networkx.DiGraph
    # which is used to draw it, (but not planned for inference)
    def root_node(self):
        return [n for n in self.nodes if self.in_degree(n) == 0][0]

    ###############################################################
    def draw_matplotlib(
        self,
        ax,
        given=None,
        computer_aliases=None,
        type_aliases=None,
        avoid_nodes_visible=False,
    ):
        # pygraphiz seems a bit of a risk as a dependency since it is not actively maintained anymore
        # for pygraphiz to work we have to translate the nodes
        # to strings  or better integers
        # ohter datatypes are not supported and of the two integers
        # are safer since not all strings go through without errors
        # H = nx.convert_node_labels_to_integers(self, label_attribute='node_label')
        # H_layout = nx.nx_pydot.pydot_layout(H, prog='dot')
        # pos = {H.nodes[n]['node_label']: p for n, p in H_layout.items()}

        nd = self.nodes.data()

        # pos = nx.circular_layout(self)
        # pos = nx.kamada_kawai_layout(self)

        # we use igraph for the layout because
        # networkx does not provide 'sugiyama' as an option
        IG = ig.Graph.from_networkx(self)
        layout = IG.layout_sugiyama()
        nl = list(self.nodes)
        pos = {nl[i]: coords for i, coords in enumerate(layout.coords)}
        type_nodes = [n for n in self.nodes if nd[n]["bipartite"] == "type"]
        given_nodes = [] if given is None else [n for n in type_nodes if n[0] in given]
        missing_nodes = (
            []
            if given is None
            else [
                n for n in type_nodes if (n[0] not in given) & (n != self.root_node())
            ]
        )
        computer_nodes = [n for n in self.nodes if nd[n]["bipartite"] == "computer"]
        ns = 100

        nx.draw_networkx_nodes(
            self,
            pos=pos,
            ax=ax,
            # nodelist=type_nodes,
            nodelist=[self.root_node()],
            node_color="red",
            node_size=ns,
            alpha=1,
            label="target type",
        )

        nx.draw_networkx_nodes(
            self,
            pos=pos,
            ax=ax,
            # nodelist=type_nodes,
            nodelist=missing_nodes,
            node_color="red",
            node_size=ns,
            alpha=0.3,
            # fixme mm:
            # we could use the structure to
            # check if a branch is computable and make it green
            # so that only the non computable nodes show as red
            label="not provided",
        )

        nx.draw_networkx_nodes(
            self,
            pos=pos,
            ax=ax,
            nodelist=computer_nodes,
            node_color="gray",
            node_size=ns,
            alpha=0.3,
            label="function",
        )

        nx.draw_networkx_nodes(
            self,
            pos=pos,
            ax=ax,
            nodelist=given_nodes,
            node_color="green",
            node_size=ns,
            label="given",
            alpha=0.3,
        )

        nx.draw_networkx_labels(
            self,
            pos=pos,
            ax=ax,
            labels={
                tn: type_node_to_str(tn, type_aliases, avoid_nodes_visible)
                for tn in type_nodes
            },
            font_color="black",
        )
        nx.draw_networkx_labels(
            self,
            pos=pos,
            ax=ax,
            labels={
                cn: computer_node_to_str(cn, computer_aliases) for cn in computer_nodes
            },
            # font_color='white'
            font_color="black",
        )
        nx.draw_networkx_edges(self, pos=pos, ax=ax, edgelist=self.edges())
        ax.legend()

    ###############################################################
    def draw_igraph(self, ax, given=None, computer_aliases=None, type_aliases=None):
        # convert the networkx graph to
        nd = self.nodes.data()

        IG = ig.Graph.from_networkx(self)
        vertex_size = [0.1 for v in IG.vs]
        labels = [v for v in IG.vs]

        # edge_color_dict = {'in':'blue','internal':'black','out':'red'}
        # edge_colors = [edge_color_dict[e['type']] for e in IG.es]
        layout = IG.layout("sugiyama")

        ig.plot(
            IG,
            layout=layout,
            vertex_size=vertex_size,
            vertex_label=labels,
            # edge_color=edge_colors
            target=ax,
        )


class TypeTree:
    # superclass only
    ############################################################################
    def dep_graph_figure(
        self, type_aliases_tup=None, computer_aliases_tup=None, given=frozenset()
    ):
        if type_aliases_tup is not None:
            type_aliases, ta_key = type_aliases_tup
        else:
            type_aliases = None

        if computer_aliases_tup is not None:
            computer_aliases, ca_key = computer_aliases_tup
        else:
            computer_aliases = None

        B = self.to_networkx_graph(avoid_types=TypeSet({}))
        nd = B.nodes.data()
        type_nodes = [n for n in B.nodes if nd[n]["bipartite"] == "type"]
        type_names = [tn[0].__name__ for tn in type_nodes]
        computer_nodes = [n for n in B.nodes if nd[n]["bipartite"] == "computer"]
        computer_names = [cn[0].__name__ for cn in computer_nodes]
        fig = plt.figure(figsize=(20, 20))
        # rect = 0, 0, 0.8, 1.2  # l, b, w, h
        rect = 0, 0, 1, 1  # l, b, w, h
        ax = fig.add_axes(rect)
        B.draw_matplotlib(
            ax,
            computer_aliases=computer_aliases,
            type_aliases=type_aliases,
            given=given,
            avoid_nodes_visible=False,
        )



        computer_aliases_by_name = {
            c.__name__: computer_aliases[c] for c, avoid_types in computer_nodes
        }

        type_aliases_by_name = {
            t.__name__: type_aliases[t] for t, avoid_types in type_nodes
        }
        # from IPython import embed; embed()

        def legend(aliases_by_name):
            if aliases_by_name is None:
                res = []
            else:
                # create in index to look up the computer from the alias
                reverse_d = {val: key for key, val in aliases_by_name.items()}
                sorted_aliases = sorted(reverse_d.keys(), key=ca_key)

                table_lines=[
                                f"{a}, {reverse_d[a]}"
                    for a in sorted_aliases
                ]
                return """\begin{tabular}
                    {'\\\\\n'.join(table_lines)}
                \end{tabular}"""

        return (
                legend(type_aliases_by_name),
                fig,
                legend(computer_aliases_by_name)
        )

    def jupyter_widget(
        self, type_aliases_tup=None, computer_aliases_tup=None, given=frozenset()
    ):
        from IPython.display import display

        if type_aliases_tup is not None:
            type_aliases, ta_key = type_aliases_tup
        else:
            type_aliases = None

        if computer_aliases_tup is not None:
            computer_aliases, ca_key = computer_aliases_tup
        else:
            computer_aliases = None

        cw1 = "20%"
        cw2 = "80%"
        cw3 = "100%"

        B = self.to_networkx_graph(avoid_types=TypeSet({}))
        nd = B.nodes.data()
        type_nodes = [n for n in B.nodes if nd[n]["bipartite"] == "type"]
        type_names = [tn[0].__name__ for tn in type_nodes]
        computer_nodes = [n for n in B.nodes if nd[n]["bipartite"] == "computer"]
        computer_names = [cn[0].__name__ for cn in computer_nodes]
        with plt.ioff():
            fig = plt.figure()  # figsize=(20, 20))
            # rect = 0, 0, 0.8, 1.2  # l, b, w, h
            rect = 0, 0, 1, 1  # l, b, w, h
            ax = fig.add_axes(rect)

        graph_out = Output(
            layout=Layout(
                height="auto",
                # width="{}%".format(thumbnail_width),
                width=cw3,
                # min_width=cw3,
                description="Dependency Tree",
            )
        )

        with graph_out:
            ax.clear()
            # ax = fig.add_subplot(1, 1, 1)
            B.draw_matplotlib(
                ax,
                computer_aliases=computer_aliases,
                type_aliases=type_aliases,
                given=given,
                avoid_nodes_visible=False,
            )
            display(ax.figure)
            plt.close(fig)

        computer_aliases_by_name = {
            c.__name__: computer_aliases[c] for c, avoid_types in computer_nodes
        }

        type_aliases_by_name = {
            t.__name__: type_aliases[t] for t, avoid_types in type_nodes
        }
        # from IPython import embed; embed()

        def legend(aliases_by_name):
            if aliases_by_name is None:
                res = []
            else:
                # create in index to look up the computer from the alias
                reverse_d = {val: key for key, val in aliases_by_name.items()}
                sorted_aliases = sorted(reverse_d.keys(), key=ca_key)

                res = VBox(
                    children=[
                        Box(
                            children=[
                                Button(
                                    layout=Layout(height="auto", min_width=cw1),
                                    description=a,
                                    button_style="warning",
                                ),
                                Button(
                                    layout=Layout(
                                        height="auto", 
                                        min_width=cw2
                                    ),
                                    description=str(reverse_d[a]),
                                    button_style="warning",
                                    color="red",
                                ),
                            ],
                            layout=Layout(
                                # overflow='scroll hidden',
                                # border='3px solid black',
                                #width='1000px',
                                width='100%',
                                height="",
                                flex_flow='row',
                                display='flex'
                            ),
                        )
                        for a in sorted_aliases
                    ]
                )
                return res

        return VBox(
            [
                Box(children=[legend(type_aliases_by_name)], layout=Layout()),
                Box(children=[graph_out], layout=Layout()),
                Box(children=[legend(computer_aliases_by_name)], layout=Layout()),
            ]
        )


class TypeNode(TypeTree):
    def __init__(self, comp_trees: List["CompTree"] = []):
        rts = set([output_mvar(ct.root_computer) for ct in comp_trees])
        if len(rts) != 1:
            raise Exception(
                "The computers of a {} have to \
                have the same result type.".format(
                    self.__class__
                )
            )
        self.comp_trees = comp_trees

    def __hash__(self):
        return sum([hash(ct) for ct in self.comp_trees.union({self.__class__})])

    def __eq__(self, other):
        return (
            self.comp_trees == other.comp_trees
            if isinstance(other, self.__class__)
            else False
        )

    def __repr__(self):
        return (
            self.__class__.__name__
            + "(\n"
            + "\tcomp_trees=frozenset({"
            + reduce(
                lambda acc, el: acc + el,
                ["\n" + add_tab(add_tab(repr(el))) + "," for el in self.comp_trees],
            )
            + "\n\t})"
            + "\n)"
        )

    @property
    def psts(self):
        # possible start types
        res = AltSet(frozenset.union(*[ct.psts for ct in self.comp_trees]))
        # from IPython import embed; embed()
        return res

    @property
    def root_type(self):
        rts = [output_mvar(ct.root_computer) for ct in self.comp_trees]
        return rts[0]

    def computable_depgraphs(self, given: TypeSet = TypeSet({})) -> MayBeDepGraphs:
        # althoug the functions t_tree and c_tree take given nodes into account
        # they don't exclude paths that need more than the given types to be
        # computable, since one of the purpuses of TypeTrees is to provide
        # information about MISSING information. The given argument here means
        # that we are only looking for depgraphs that can actually be used to
        # compute the value of the variable at the top of the TypeTree.

        dep_graph_sets = [ct.computable_depgraphs(given) for ct in self.comp_trees]
        # from IPython import embed;embed()

        return JustDepGraphs(
            reduce(
                lambda acc, el: acc.union(el.result_set), dep_graph_sets, frozenset()
            )
        )

    def to_networkx_graph(self, avoid_types):
        g = OrGraphNX()
        root_type = self.root_type
        node = (root_type, avoid_types)
        g.add_node(node, bipartite="type")
        for ct in self.comp_trees:
            sub_graph = ct.to_networkx_graph(avoid_types.union({root_type}))
            g = nx.compose(g, sub_graph)
            g.add_edge(node, sub_graph.root_node())

        return g


class TypeLeaf(TypeTree):
    def __init__(self, root_type: type):
        self.root_type = root_type

    def __hash__(self):
        return hash(self.__class__) + hash(self.root_type)

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.root_type.__name__ + ")"

    def __eq__(self, other):
        return (
            self.root_type == other.root_type
            if self.__class__ == other.__class__
            else False
        )

    @property
    def psts(self):
        # possible start types
        return AltSet([TypeSet([self.root_type])])

    def computable_depgraphs(self, given: TypeSet = TypeSet({})) -> MayBeDepGraphs:
        if self.root_type in given:
            return JustDepGraphs(frozenset({DepGraph()}))
        else:
            return NoDepGraphs()

    def to_networkx_graph(self, avoid_types):
        g = OrGraphNX()
        root_type = self.root_type
        node = (root_type, avoid_types)
        g.add_node(node, bipartite="type")
        return g

    # def to_igraph_graph(self):
    #    g = OrGraphNX()
    #    root_type = self.root_type
    #    g.add_node(root_type, bipartite="type")
    #    return g


class CompTree:
    def __init__(self, root_computer: Callable, type_trees: List[TypeTree]):
        # remembering the root_computer is not strictly necessary
        # but nice for drawing
        # We could also link upwards to it to make the tree traversable
        # in both directions
        self.root_computer = root_computer
        self.type_trees = type_trees

    def __eq__(self, other):
        return (
            (
                (self.type_trees == other.type_trees)
                and (self.root_computer == other.root_computer)
            )
            if isinstance(other, self.__class__)
            else False
        )

    def __hash__(self):
        return sum(
            [
                hash(v)
                for v in (self.type_trees.union({self.__class__, self.root_computer}))
            ]
        )

    @property
    def psts(self) -> "AltSet[TypeSet]":
        # possible start types
        # every element of sss is a set of sets
        ass = AltSetSet([tt.psts for tt in self.type_trees])
        res = ass.combine()
        return res

    def __repr__(self):
        return (
            self.__class__.__name__
            + "(\n"
            + "\troot_computer="
            + self.root_computer.__name__
            + ",\n"
            + "\ttype_trees=frozenset({"
            + reduce(
                lambda acc, el: acc + el,
                ["\n" + add_tab(add_tab(repr(el))) + "," for el in self.type_trees],
            )
            + "\n\t})"
            + "\n)"
        )

    def computable_depgraphs(self, given: TypeSet = TypeSet({})) -> MayBeDepGraphs:

        # first check that we compute everything we need
        if any(
            (
                isinstance(tt.computable_depgraphs(given), NoDepGraphs)
                for tt in self.type_trees
            )
        ):
            return NoDepGraphs()
        else:
            # now we look at the possible combinations to provide the arguments
            ass = [tt.computable_depgraphs(given).dep_graphs for tt in self.type_trees]
            tup_list = list_mult2(ass)

            rc = self.root_computer

            def extend_sub_dgs(sub_dgs):
                dg = DepGraph()
                dg.add_node(rc)
                for sdg in sub_dgs:
                    if len(sdg.nodes) > 0:
                        dg.update(sdg)
                        dg.add_edge(rc, sdg.root_node())
                return dg

            extended = tuple((extend_sub_dgs(sdgs) for sdgs in tup_list))
            # from IPython import embed;embed()
            return JustDepGraphs(extended)

    def to_networkx_graph(self, avoid_types):
        g = OrGraphNX()
        root_computer = self.root_computer
        node = (root_computer, avoid_types)
        g.add_node(node, bipartite="computer")
        if self.type_trees != []:
            for tt in self.type_trees:
                sub_graph = tt.to_networkx_graph(avoid_types)
                g = nx.compose(g, sub_graph)
                g.add_edge(node, sub_graph.root_node())
        return g


# pair of recursive functions t_tree and c_tree to generate the datastructure
# from a given target type
def t_tree(
    root_type: type,
    available_computers: ComputerSet = ComputerSet({}),
    avoid_types: Set[type] = frozenset(),
    given_types: Set[type] = frozenset(),
) -> TypeTree:
    def fi(c):
        return (
            output_mvar(c) == root_type
            and len(input_mvars(c).intersection(avoid_types)) == 0
            and output_mvar(c) not in given_types
        )

    available_result_computers = tuple(filter(fi, available_computers))
    # from IPython import embed; embed()
    if len(available_result_computers) == 0:  # stop recursion
        return TypeLeaf(root_type)
    else:
        return TypeNode(
            comp_trees=frozenset(
                [
                    c_tree(
                        c=c,
                        available_computers=available_computers.difference({c}),
                        avoid_types=avoid_types.union({root_type}),
                        given_types=given_types,
                    )
                    for c in available_result_computers
                ]
            ),
        )


def c_tree(
    c: Callable,
    available_computers: ComputerSet,
    avoid_types: List[type],
    given_types: Set[type] = frozenset(),
) -> CompTree:
    res_type = output_mvar(c)
    argset = input_mvars(c)
    return CompTree(
        root_computer=c,
        type_trees=frozenset(
            [
                t_tree(
                    root_type=v,
                    available_computers=available_computers,
                    avoid_types=avoid_types,
                    given_types=given_types,
                )
                for v in argset
            ]
        ),
    )
