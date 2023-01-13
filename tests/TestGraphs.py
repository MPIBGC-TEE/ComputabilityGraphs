#!/usr/bin/env python3
import matplotlib.pyplot as plt
from frozendict import frozendict
from copy import copy, deepcopy
import networkx as nx
from testinfrastructure.InDirTest import InDirTest
from testinfrastructure.helpers import pp, pe
from unittest import skip
from copy import copy, deepcopy

from ComputabilityGraphs.graph_helpers import (
    toDiGraph,
    equivalent_multigraphs,
)


from testComputers import A, B, X, Y
from testComputers import computers
from testComputers import (
    a_from_x,
    b_from_y,
    a_from_y,
    b_from_x,
)


class TestGraphs(InDirTest):
    def setUp(self):
        self.computers = computers

    def test_toDiGraph(self):
        g_multi = nx.MultiDiGraph()
        src = frozenset({X, Y})
        dest = frozenset({A, B})
        computers_1 = frozenset({a_from_x, b_from_y})

        computers_2 = frozenset({a_from_y, b_from_x})
        g_multi.add_edge(src, dest, computers=computers_1)
        g_multi.add_edge(src, dest, computers=computers_2)
        g_single = toDiGraph(g_multi)
        self.assertSetEqual(
            g_single.get_edge_data(src, dest)["computers"],
            frozenset({computers_1, computers_2}),
        )

    def test_equivalent_multigraphs(self):
        g1 = nx.MultiDiGraph()
        g1.add_edge(
            frozenset({X, Y}),
            frozenset({A, B}),
            computers=frozenset({a_from_x, b_from_y}),
        )
        g1.add_edge(
            frozenset({X, Y}),
            frozenset({A, B}),
            computers=frozenset({a_from_y, b_from_x}),
        )

        g2 = deepcopy(g1)
        # now we exchange the edge data
        g2.add_edge(
            frozenset({X, Y}),
            frozenset({A, B}),
            computers=frozenset({a_from_y, b_from_x}),
        )
        g2.add_edge(
            frozenset({X, Y}),
            frozenset({A, B}),
            computers=frozenset({a_from_x, b_from_y}),
        )

        self.assertTrue(equivalent_multigraphs(g1, g2))

    # def test_arg_set_graph(self):
    #    asg = arg_set_graph(D, self.computers)
    #    # For compatibility arg_set_graph returns a multigraph
    #    # although we do not have more than one edge between a pair
    #    # of nodes.

    #    ref = nx.MultiDiGraph()
    #    ref.add_edge(
    #        frozenset({B}),
    #        frozenset({D}),
    #        computers=frozenset({d_from_b})
    #    )
    #    ref.add_edge(
    #        frozenset({G, H}),
    #        frozenset({D}),
    #        computers=frozenset({d_from_g_h})
    #    )

    #    # picture for manual check
    #    fig = plt.figure(figsize=(20, 20))
    #    ax1 = fig.add_subplot(1, 2, 1)
    #    ax2 = fig.add_subplot(1, 2, 2)
    #    draw_ComputerSetMultiDiGraph_matplotlib(ax1, ref)
    #    draw_ComputerSetMultiDiGraph_matplotlib(ax2, asg)
    #    fig.savefig("arg_set_graph.pdf")

    #    self.assertTrue(equivalent_multigraphs(asg, ref))
