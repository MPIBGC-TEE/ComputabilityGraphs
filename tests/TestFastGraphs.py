#!/usr/bin/env python3
import matplotlib.pyplot as plt
from frozendict import frozendict
from copy import copy, deepcopy
import networkx as nx
from networkx.algorithms import bipartite
from testinfrastructure.InDirTest import InDirTest
from testinfrastructure.helpers import pp, pe
from unittest import skip
from copy import copy, deepcopy

#from ComputabilityGraphs.graph_helpers import (
#    arg_set_graph,
#    initial_sparse_powerset_graph,
#    minimal_startnodes_for_single_var,
#    minimal_startnodes_for_node,
#    update_step,
#    toDiGraph,
#    equivalent_singlegraphs,
#    equivalent_multigraphs,
#    node_2_string,
#    nodes_2_string,
#    edge_2_string,
#    product_graph,
#    sparse_powerset_graph,
#    update_generator,
#    # draw_multigraph_plotly,
#    # draw_Graph_svg,
#)
from ComputabilityGraphs.graph_plotting import (
     draw_FastGraph_matplotlib,
#    draw_update_sequence,
#    draw_ComputerSetDiGraph_matplotlib,
    draw_ComputerSetMultiDiGraph_matplotlib
)
#from ComputabilityGraphs.non_graph_helpers import arg_set_set, all_mvars
#
from testComputers import  A, A1, A2, A3, A0, A_minus_1, A_minus_2, B, B1, B2, B3, B0, B_minus_1, B_minus_2, C, D, E, F, G, H, I, X, Y
from testComputers import computers
from testComputers import ( 
    a_from_x,
    b_from_y,
    a_from_y,
    b_from_x,
    a_from_z,
    b_from_z,
    c_from_b,
    d_from_b,
    d_from_g_h,
    a2_from_a1,
    a3_from_a2,
    b_minus_1_from_b_minus_2,
    b0_from_b_minus_1,
    a_minus_1_from_a_minus_2,
    a1_from_a0,
    a0_from_a_minus_1,
    b1_from_b0,
    b2_from_b1,
    b3_from_b2,
    a0_from_b0
)


class TestFastGraphs(InDirTest):
    def setUp(self):
        self.computers = computers

    def test_project(self):
        # project the bipartite graph consisting of 
        # two kinds of nodes (sets and decompositions)
        # to the graph we actually need which has only sets

        # var set
        sn1 = frozenset([A3, B1])
        sn11 = frozenset([A2, B0])
        sn12 = frozenset([A2, B1])
        sn13 = frozenset([A3, B0])
        # decomposition
        dn1 = (
            frozenset([A3, B1]),    # active
            frozenset([])           # passive
        )
        dn2 = (
            frozenset([A3]),        # active
            frozenset([B1])         # pass
        )
        dn3 = (
            frozenset([B1]),        # active
            frozenset([A3])         # pass
        )
        g = nx.DiGraph()
        g.add_node(sn1, bipartite=0)

        g.add_node(dn1, bipartite=1)
        g.add_edge(dn1, sn1)
        g.add_node(sn11, bipartite=0)

        g.add_node(dn2, bipartite=1)
        g.add_edge(dn2, sn1)
        g.add_node(sn12, bipartite=0)

        g.add_node(dn3, bipartite=1)
        g.add_edge(dn3, sn1)
        g.add_node(sn13, bipartite=0)

        g.add_edge(
            sn11,
            dn1,
            computers=frozenset({a3_from_a2, b1_from_b0})
        )
        g.add_edge(
            sn12,
            dn2,
            computers=frozenset({a3_from_a2})
        )
        g.add_edge(
            sn13,
            dn3,
            computers=frozenset({b1_from_b0})
        )
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        (sets,partitions) = bipartite.sets(g) 
        # or alternatively
        top_nodes = {n for n, d in g.nodes(data=True) if d["bipartite"] == 0}

        bottom_nodes = set(g) - top_nodes
        #g_new = replaceNode(src=A2,repl=
        G = bipartite.projected_graph(g, top_nodes)

        draw_ComputerSetMultiDiGraph_matplotlib(
            ax2,
            G
        )
        fig.savefig("projection.pdf")
