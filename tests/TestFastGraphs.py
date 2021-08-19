#!/usr/bin/env python3
import matplotlib.pyplot as plt
from frozendict import frozendict
from copy import copy, deepcopy
import networkx as nx
from networkx.algorithms import bipartite
from testinfrastructure.InDirTest import InDirTest
from testinfrastructure.helpers import pp, pe
from unittest import skip
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

class TestFastGraph1(InDirTest):
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

    

    def test_add_all_arg_set_graphs_to_decomp_1(self):
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

        #g.add_node(sn11, bipartite=0) # unneccessary because sn11 is a superset of sn12, sn13


        fig = plt.figure(figsize=(30, 10))
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
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

    def test_add_all_arg_set_graphs_to_decomp_2(self):
        # var set
        sn1 = frozenset([A3, B1])
        sn11 = frozenset([A2, B0])
        sn12 = frozenset([A2, B1])
        sn13 = frozenset([B0, B1])
        dn1 = (
            frozenset([A3]),        # active
            frozenset([B1])         # pass
        )
        g = nx.DiGraph()
        g.add_node(sn1, bipartite=0)

        g.add_node(dn1, bipartite=1)
        g.add_edge(dn1, sn1)

        #g.add_node(sn11, bipartite=0)


        fig = plt.figure(figsize=(30, 10))
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        
        G_ref=deepcopy(g)
        G_ref.add_node(sn12, bipartite=0)
        G_ref.add_node(sn13, bipartite=0)
        G_ref.add_edge(
            sn12,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_a2})
            })
        )
        G_ref.add_edge(
            sn13,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_b0}),
            })
        )
        draw_FastGraph_matplotlib(
            ax2,
            G_ref,
        )



        computers = frozenset([
            tC.a3_from_a2,
            tC.a3_from_b0,
            tC.b1_from_b0,
            tC.b1_from_a2
        ])
        
        g_res, new_set = add_all_arg_set_graphs_to_decomp(
            g,
            dn1,
            computers
        )
        draw_FastGraph_matplotlib(
            ax3,
            g_res,
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

    def test_add_decompositions_arg_set_graphs(self):

        # var set
        sn1 = frozenset([A3, B1])
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
        g_base = nx.DiGraph()
        g_base.add_node(sn1, bipartite=0)

        g_base.add_node(dn1, bipartite=1)
        g_base.add_edge(dn1, sn1)

        g_base.add_node(dn2, bipartite=1)
        g_base.add_edge(dn2, sn1)

        g_base.add_node(dn3, bipartite=1)
        g_base.add_edge(dn3, sn1)
        
        g_ref = deepcopy(g_base)
        sn111 = frozenset([A2])
        g_ref.add_node(sn111, bipartite=0)
        g_ref.add_edge(
            sn111,
            dn1,
            computer_sets = frozenset([
                frozenset({tC.a3_from_a2, tC.b1_from_a2})
            ])
        )
        sn112 = frozenset([B0])
        g_ref.add_node(sn112, bipartite=0)
        g_ref.add_edge(
            sn112,
            dn1,
            computer_sets = frozenset([
                frozenset({tC.a3_from_b0, tC.b1_from_b0})
            ])
        )
        sn121 = frozenset([A2, B1])
        g_ref.add_node(sn121, bipartite=0)
        g_ref.add_edge(
            sn121,
            dn2,
            computer_sets = frozenset([
                frozenset({tC.a3_from_a2})
            ])
        )
        sn122 = frozenset([B0, B1])
        g_ref.add_node(sn122, bipartite=0)
        g_ref.add_edge(
            sn122,
            dn2,
            computer_sets = frozenset([
                frozenset({tC.a3_from_b0})
            ])
        )
        sn131 = frozenset([A3, B0])
        g_ref.add_node(sn131, bipartite=0)
        g_ref.add_edge(
            sn131,
            dn3,
            computer_sets = frozenset([
                frozenset({tC.b1_from_b0})
            ])
        )
        sn132 = frozenset([A3, A2])
        g_ref.add_node(sn132, bipartite=0)
        g_ref.add_edge(
            sn132,
            dn3,
            computer_sets = frozenset([
                frozenset({tC.b1_from_a2})
            ])
        )
        new_nodes_ref = frozenset([sn111, sn112, sn121, sn122, sn131, sn132])
        fig = plt.figure(figsize=(30, 20))
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        draw_FastGraph_matplotlib(
            ax1,
            g_base
        )
        draw_FastGraph_matplotlib(
            ax2,
            g_ref
        )
        computers = frozenset([
            tC.a3_from_a2,
            tC.a3_from_b0,
            tC.b1_from_b0,
            tC.b1_from_a2
        ])
        g_res, new_nodes_res = fgh.add_arg_set_graphs_to_decomps(
            g_base,
            decomps=frozenset([dn1, dn2, dn3]),
            all_computers = computers
        )
        draw_FastGraph_matplotlib(
            ax3,
            g_res
        )
        fig.savefig("figure.pdf")
        self.assertTrue(
            equivalent_singlegraphs(
                g_ref,
                g_res
            )
        )
        self.assertEqual(
            new_nodes_ref,
            new_nodes_res
        )

class TestFastGraph2(InDirTest):   

    def setUp(self):
        self.computers = frozenset({
            tC.a_from_e_f,
            tC.a_from_g_h,
            tC.b_from_i_j,
            tC.j_from_g,
            tC.b_from_c_d
        })


    def test_uncomputable(self):
        computers = self.computers
        self.assertEqual(
            h.uncomputable(computers),
            frozenset({C, C, D, E, F, G, H, I})
        )
    
    def test_add_all_decompositions_to_node(self):
        g_base = nx.DiGraph()
        # var set
        sn1 = frozenset([A, B, C])
        g_base.add_node(sn1, bipartite=0)
        
        g_ref = deepcopy(g_base)
        # decompositions
        decompositions = frozenset([
            (
                frozenset([A, B, C]),    # active
                frozenset([])           # passive
            ),
            (
                frozenset([A, B]),    # active
                frozenset([C])           # passive
            ),
            (
                frozenset([C]),    # active
                frozenset([A, B])           # passive
            ),
            (
                frozenset([A, C]),    # active
                frozenset([B])           # passive
            ),
            (
                frozenset([B]),    # active
                frozenset([A,C])           # passive
            ),
            (
                frozenset([B, C]),    # active
                frozenset([A])           # passive
            ),
            (
                frozenset([A]),    # active
                frozenset([B,C])           # passive
            ),
            (
                frozenset([]),    # active
                frozenset([A, B, C])           # passive
            )
        ])

        for dn in decompositions:
            g_ref.add_node(dn, bipartite=1)
            g_ref.add_edge(dn, sn1)


        fig = plt.figure(figsize=(30, 20))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        draw_FastGraph_matplotlib(
            ax1,
            g_ref,
        )
        uncomputable = frozenset([])
        g = deepcopy(g_base)
        g_res, new_decompositions = fgh.add_all_decompositions_to_node(g, sn1, uncomputable)
        draw_FastGraph_matplotlib(
            ax2,
            g_res,
        )
        fig.savefig("figure.pdf")
        self.assertTrue(
            equivalent_singlegraphs(
                g_ref,
                g_res
            )
        )
        print(frozenset.difference(new_decompositions, decompositions))
        print(frozenset.difference(decompositions, new_decompositions))
        self.assertEqual(
            decompositions,
            new_decompositions
        )

    def test_add_all_decompositions_to_node_with_uncomputables(self):
        g_base = nx.DiGraph()
        # var set
        sn1 = frozenset([A, B, C])
        g_base.add_node(sn1, bipartite=0)
        
        g_ref = deepcopy(g_base)
        # decompositions 
        # Note that the decomposition with uncomputable variables in th active part are cleaned out
        decompositions = frozenset([
            #(
            #    frozenset([A, B, C]),    # active
            #    frozenset([])           # passive
            #),
            (
                frozenset([A, B]),    # active
                frozenset([C])           # passive
            ),
            #(
            #    frozenset([C]),    # active
            #    frozenset([A, B])           # passive
            #),
            #(
            #    frozenset([A, C]),    # active
            #    frozenset([B])           # passive
            #),
            (
                frozenset([B]),    # active
                frozenset([A,C])           # passive
            ),
            #(
            #    frozenset([B, C]),    # active
            #    frozenset([A])           # passive
            #),
            (
                frozenset([A]),    # active
                frozenset([B,C])           # passive
            ),
            (
                frozenset([]),    # active
                frozenset([A, B, C])           # passive
            )
        ])

        for dn in decompositions:
            g_ref.add_node(dn, bipartite=1)
            g_ref.add_edge(dn, sn1)


        fig = plt.figure(figsize=(30, 20))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        draw_FastGraph_matplotlib(
            ax1,
            g_ref,
        )
        uncomputable = frozenset([C])
        g = deepcopy(g_base)
        g_res, new_decompositions = fgh.add_all_decompositions_to_node(g, sn1, uncomputable)
        draw_FastGraph_matplotlib(
            ax2,
            g_res,
        )
        fig.savefig("figure.pdf")
        self.assertTrue(
            equivalent_singlegraphs(
                g_ref,
                g_res
            )
        )
        print(frozenset.difference(new_decompositions, decompositions))
        print(frozenset.difference(decompositions, new_decompositions))
        self.assertEqual(
            decompositions,
            new_decompositions
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

        new_decompositions = frozenset(
            [
                (frozenset([v]), frozenset([])) 
                for v in [A, B, J]
            ]
        )
        for dn in new_decompositions: 
            g.add_node(dn, bipartite=1)
            g.add_edge(dn, dn[0])

        g_res,new_decompositions_res  = fgh.initial_fast_graph(computers)
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        draw_FastGraph_matplotlib(
            ax2,
            g_res,
        )
        fig.savefig("figure.pdf")

        self.assertTrue(
            equivalent_singlegraphs(
                g_res,
                g
            )
        )
        self.assertTrue(
            new_decompositions,
            new_decompositions_res
        )

    def test_fast_graph(self):
        computers = self.computers
        g = nx.DiGraph()
        for v in [A, B, C, D, E, F, G, H, I, J]:
            g.add_node(frozenset({v}), bipartite=0)

        new_decompositions = frozenset(
            [
                (frozenset([v]), frozenset([])) 
                for v in [A, B, J]
            ]
        )
        for dn in new_decompositions: 
            g.add_node(dn, bipartite=1)
            g.add_edge(dn, dn[0])

        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        draw_FastGraph_matplotlib(
            ax1,
            g,
        )
        #from IPython import embed; embed()
        g_res = fgh.fast_graph(computers)
        draw_FastGraph_matplotlib(
            ax2,
            g_res,
        )
        fig.savefig("figure.pdf")
        
