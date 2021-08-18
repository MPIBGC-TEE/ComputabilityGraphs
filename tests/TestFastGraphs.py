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
from ComputabilityGraphs.fast_graph_helpers import (
        add_combi_arg_set_graph,
        add_combis_arg_set_graphs_to_decomp,
        add_all_arg_set_graphs_to_decomp,
)
import ComputabilityGraphs.fast_graph_helpers as fgh
from ComputabilityGraphs.graph_helpers import (
#    arg_set_graph,
#    initial_sparse_powerset_graph,
#    minimal_startnodes_for_single_var,
#    minimal_startnodes_for_node,
#    update_step,
#    toDiGraph,
     equivalent_singlegraphs#,
#    equivalent_multigraphs,
#    node_2_string,
#    nodes_2_string,
#    edge_2_string,
#    product_graph,
#    sparse_powerset_graph,
#    update_generator,
#    # draw_multigraph_plotly,
#    # draw_Graph_svg,
)
from ComputabilityGraphs.graph_plotting import (
     draw_FastGraph_matplotlib,
#    draw_update_sequence,
#    draw_ComputerSetDiGraph_matplotlib,
    draw_ComputerSetMultiDiGraph_matplotlib
)
import ComputabilityGraphs.helpers as h

from testComputers import (
        A, A1, A2, A3, A0, A_minus_1, A_minus_2, B,
        B1, B2, B3, B0, B_minus_1, B_minus_2, C, D, E, F, G, H, I,J, X, Y)
# from testComputers import computers
import testComputers as tC

class TestFastGraphs(InDirTest):
    def setUp(self):
        self.computers = tC.computers

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
            computers=frozenset({tC.a3_from_a2, tC.b1_from_b0})
        )
        g.add_edge(
            sn12,
            dn2,
            computers=frozenset({tC.a3_from_a2})
        )
        g.add_edge(
            sn13,
            dn3,
            computers=frozenset({tC.b1_from_b0})
        )
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        (sets, partitions) = bipartite.sets(g)
        # or alternatively
        top_nodes = {n for n, d in g.nodes(data=True) if d["bipartite"] == 0}

        bottom_nodes = set(g) - top_nodes
        #g_new = replaceNode(src=A2, repl=
        G = bipartite.projected_graph(g, top_nodes)

        draw_ComputerSetMultiDiGraph_matplotlib(
            ax2,
            G
        )
        fig.savefig("figure.pdf")

    def test_add_arg_set(self):
        # var set
        sn1 = frozenset([A3, B1])
        sn11 = frozenset([A2, B0])
        # decomposition
        dn1 = (
            frozenset([A3, B1]),    # active
            frozenset([])           # passive
        )
        g = nx.DiGraph()
        g.add_node(sn1, bipartite=0)

        g.add_node(dn1, bipartite=1)
        g.add_edge(dn1, sn1)


        fig = plt.figure(figsize=(10, 30))
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        G, new_set = add_combi_arg_set_graph(
            g,
            dn1,
            frozenset({tC.a3_from_a2, tC.b1_from_b0})
        )
        draw_FastGraph_matplotlib(
            ax2,
            G,
        )
        G_ref=deepcopy(g)
        G_ref.add_node(sn11, bipartite=0)
        G_ref.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        draw_FastGraph_matplotlib(
            ax3,
            G_ref,
        )
        fig.savefig("figure.pdf")
        G, new_set = add_combi_arg_set_graph(
            g,
            dn1,
            frozenset({tC.a3_from_a2, tC.b1_from_b0})
        )
        draw_FastGraph_matplotlib(
            ax2,
            G,
        )
        G_ref=deepcopy(g)
        G_ref.add_node(sn11, bipartite=0)
        G_ref.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        draw_FastGraph_matplotlib(
            ax3,
            G_ref,
        )
        fig.savefig("figure.pdf")
        self.assertTrue(equivalent_singlegraphs(G, G_ref))
        self.assertEqual(new_set, frozenset({sn11}))

    def test_add_arg_set_overlapping(self):
        # var set
        sn1 = frozenset([A3, B1])
        sn11 = frozenset([A2, B0])
        # decomposition
        dn1 = (
            frozenset([A3, B1]),    # active
            frozenset([])           # passive
        )
        g = nx.DiGraph()
        g.add_node(sn1, bipartite=0)

        g.add_node(dn1, bipartite=1)
        g.add_edge(dn1, sn1)

        g.add_node(sn11, bipartite=0)
        g.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )

        fig = plt.figure(figsize=(10, 30))
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        G, new_set = add_combi_arg_set_graph(
            g,
            dn1,
            frozenset({tC.a3_from_b0, tC.b1_from_a2})
        )
        draw_FastGraph_matplotlib(
            ax2,
            G,
        )

        G_ref = deepcopy(g)
        G_ref.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_b0, tC.b1_from_a2}),
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        draw_FastGraph_matplotlib(
            ax3,
            G_ref,
        )
        fig.savefig("figure.pdf")
        self.assertTrue(equivalent_singlegraphs(G, G_ref))
        self.assertEqual(new_set, frozenset({}))

    def test_add_combis_arg_set_graphs(self):
        # var set
        sn1 = frozenset([A3, B1])
        sn11 = frozenset([A2, B0])
        # decomposition
        dn1 = (
            frozenset([A3, B1]),    # active
            frozenset([])           # passive
        )
        g = nx.DiGraph()
        g.add_node(sn1, bipartite=0)

        g.add_node(dn1, bipartite=1)
        g.add_edge(dn1, sn1)

        g.add_node(sn11, bipartite=0)


        fig = plt.figure(figsize=(10, 30))
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        G, new_set = add_combis_arg_set_graphs_to_decomp(
            g,
            dn1,
            frozenset({
                frozenset({tC.a3_from_b0, tC.b1_from_a2}),
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        draw_FastGraph_matplotlib(
            ax2,
            G,
        )

        G_ref=deepcopy(g)
        G_ref.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_b0, tC.b1_from_a2}),
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        draw_FastGraph_matplotlib(
            ax3,
            G_ref,
        )
        fig.savefig("figure.pdf")
        self.assertTrue(equivalent_singlegraphs(G, G_ref))
        self.assertEqual(new_set, frozenset({sn11}))

    def test_all_computer_combis_for_mvar_set(self):
        computers = frozenset([
            tC.a3_from_a2,
            tC.a3_from_b0,
            tC.b1_from_b0,
            tC.b1_from_a2])
        var_set = frozenset({A3, B1})
        self.assertEqual(
            h.all_computer_combis_for_mvar_set(var_set, computers),
            frozenset({
                frozenset({tC.a3_from_a2, tC.b1_from_b0}),
                frozenset({tC.a3_from_a2, tC.b1_from_a2}),
                frozenset({tC.a3_from_b0, tC.b1_from_a2}),
                frozenset({tC.a3_from_b0, tC.b1_from_b0})
                })
        )

    def test_add_all_arg_set_graphs_to_decomp(self):
        # var set
        sn1 = frozenset([A3, B1])
        sn11 = frozenset([A2, B0])
        sn12 = frozenset([A2])
        sn13 = frozenset([B0])
        # decomposition
        dn1 = (
            frozenset([A3, B1]),    # active
            frozenset([])           # passive
        )
        g = nx.DiGraph()
        g.add_node(sn1, bipartite=0)

        g.add_node(dn1, bipartite=1)
        g.add_edge(dn1, sn1)

        #g.add_node(sn11, bipartite=0)


        fig = plt.figure(figsize=(10, 30))
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        computers = frozenset([
            tC.a3_from_a2,
            tC.a3_from_b0,
            tC.b1_from_b0,
            tC.b1_from_a2])
        g_res, new_set = add_all_arg_set_graphs_to_decomp(
            g,
            dn1,
            computers
        )
        draw_FastGraph_matplotlib(
            ax2,
            g_res,
        )

        G_ref=deepcopy(g)
        G_ref.add_node(sn12, bipartite=0)
        G_ref.add_node(sn13, bipartite=0)
        G_ref.add_edge(
            sn12,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_a2, tC.b1_from_a2})
            })
        )
        G_ref.add_edge(
            sn13,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_b0, tC.b1_from_b0}),
            })
        )
        draw_FastGraph_matplotlib(
            ax3,
            G_ref,
        )
        fig.savefig("figure.pdf")
        self.assertTrue(equivalent_singlegraphs(g_res, G_ref))
        self.assertEqual(
                new_set,
                frozenset({
                    sn12,
                    sn13
                })
        )

    @skip("not complete yet")
    def test_add_decompositions_arg_set_graphs(self):

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
            computers=frozenset({tC.a3_from_a2, tC.b1_from_b0})
        )
        g.add_edge(
            sn12,
            dn2,
            computers=frozenset({tC.a3_from_a2})
        )
        g.add_edge(
            sn13,
            dn3,
            computers=frozenset({tC.b1_from_b0})
        )
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        fig.savefig("figure.pdf")


class TestFastGraph2(InDirTest):   

    def setUp(self):
        self.computers = frozenset({
            tC.a_from_e_f,
            tC.a_from_g_h,
            tC.b_from_i_j,
            tC.j_fro_g,
            tC.b_from_c_d
        })


    def test_uncomputable(self):
        computers = self.computers
        self.assertEqual(
            h.uncomputable(computers),
            frozenset({C, C, D, E, F, G, H, I})
        )
    
    def test_plot(self):
        g = nx.DiGraph()
        for v in [A, B, C, D, E, F, G, H, I, J]:
            n = frozenset([v,])
            g.add_node(n, bipartite=0)

        for v in [A, B, J]:
            n = frozenset([v,])
            dn = (
                    n,
                    frozenset([])
            )
            g.add_node(dn, bipartite=1)
            g.add_edge(dn, n)

        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(1, 1, 1)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        fig.savefig("figure.pdf")

  
    def test_initial_fast_graph(self):
        computers = self.computers
        g = nx.DiGraph()
        for v in [A, B, C, D, E, F, G, H, I, J]:
            g.add_node(frozenset([v]), bipartite=0)

        for v in [A, B, J]:
            n = frozenset([v])
            dn = (n,frozenset([]))
            g.add_node(dn, bipartite=1)
            g.add_edge(dn, n)

        res = fgh.initial_fast_graph(computers)
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        #from IPython import embed; embed()
        draw_FastGraph_matplotlib(
            ax2,
            res,
        )
        fig.savefig("figure.pdf")

        self.assertTrue(
            equivalent_singlegraphs(
                res,
                g
            )
        )

    def test_fast_graph(self):
        computers = self.computers
        # g = fgh.fast_graph(computers)
        g = nx.DiGraph()
        for v in [A, B, C, D, E, F, G, H, I, J]:
            g.add_node(frozenset({v}), bipartite=0)

        for v in [A, B, J]:
            n = frozenset({v})
            dn = (n,frozenset([]))
            g.add_node(dn, bipartite=1)
            g.add_edge(dn, n)

