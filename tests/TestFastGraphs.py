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
from ComputabilityGraphs.graph_plotting import (
    draw_ComputerSetMultiDiGraph_matplotlib
)
from ComputabilityGraphs.FastGraph import FastGraph
import ComputabilityGraphs.helpers as h

from testComputers import (
        A, A1, A2, A3, A0, A_minus_1, A_minus_2, B,
        B1, B2, B3, B0, B_minus_1, B_minus_2, C, D, E, F, G, H, I,J, X, Y)
# from testComputers import computers
import testComputers as tC

class TestFastGraph(InDirTest):
    def setUp(self):
        self.computers = tC.computers

    def test_init(self):
        g = FastGraph()
        
        self.assertEqual(
            g.get_Nodes(),
            frozenset([])
        )
        self.assertEqual(
            g.get_Decomps(),
            frozenset([])
        )

    def test_add_Node(self):
        g = FastGraph()
        n = frozenset([tC.A, tC.B])
        g.add_Node(n)
        

    def test_add_Decomp(self):
        g = FastGraph()
        s1 = frozenset([tC.A])
        s2 = frozenset([tC.B])
        n = frozenset.union(s1,s2)
        d = (s1,s2) 
        g.add_Decomp(targetNode=n,decomp=d)
    
    def test_draw_empty(self):
        # test empty graph
        g = FastGraph()
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(1, 1, 1)
        g.draw_matplotlib(
            ax1,
        )
        fig.savefig("figure.pdf")

    def test_draw_only_nodes(self):
        # test empty graph
        g = FastGraph()
        n = frozenset([tC.A, tC.B])
        g.add_Node(n)
        
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(1, 1, 1)
        g.draw_matplotlib(
            ax1,
        )
        fig.savefig("figure.pdf")
    
    def test_draw(self):
        # test empty graph
        g = FastGraph()
        s1 = frozenset([tC.A])
        s2 = frozenset([tC.B])
        n = frozenset.union(s1,s2)
        d = (s1,s2) 
        g.add_Node(n)
        g.add_Decomp(targetNode=n,decomp=d)
        
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(1, 1, 1)
        g.draw_matplotlib(
            ax1,
        )
        fig.savefig("figure.pdf")


  
    
    @skip("the computersets projection is not yet implemented")
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

class TestFastGraph1(InDirTest):

    def test_add_arg_set(self):
        # var set
        sn1 = frozenset([A3, B1])
        sn11 = frozenset([A2, B0])
        # decomposition
        dn1 = (
            frozenset([A3, B1]),    # active
            frozenset([])           # passive
        )
        g = FastGraph()
        g.add_Node(sn1)
        g.add_Decomp(sn1, dn1)


        fig = plt.figure(figsize=(10, 30))
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        g.draw_matplotlib(ax1)
        G, new_set = add_combi_arg_set_graph(
            g,
            dn1,
            frozenset({tC.a3_from_a2, tC.b1_from_b0})
        )
        G.draw_matplotlib(ax2)
        
        G_ref=deepcopy(g)
        G_ref.add_Node(sn11)
        G_ref.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        G_ref.draw_matplotlib(ax3)
        
        G, new_set = add_combi_arg_set_graph(
            g,
            dn1,
            frozenset({tC.a3_from_a2, tC.b1_from_b0})
        )
        G.draw_matplotlib(ax2)

        G_ref=deepcopy(g)
        G_ref.add_Node(sn11)
        G_ref.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        G_ref.draw_matplotlib(ax3)

        fig.savefig("figure.pdf")
        self.assertEqual(G, G_ref)
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
        g = FastGraph()
        g.add_Node(sn1)

        g.add_Decomp(sn1, dn1)

        g.add_Node(sn11)
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
        g.draw_matplotlib(ax1)
        G, new_set = add_combi_arg_set_graph(
            g,
            dn1,
            frozenset({tC.a3_from_b0, tC.b1_from_a2})
        )
        G.draw_matplotlib(ax2)

        G_ref = deepcopy(g)
        G_ref.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_b0, tC.b1_from_a2}),
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        G_ref.draw_matplotlib(ax3)
        fig.savefig("figure.pdf")
        self.assertEqual(G, G_ref)
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
        g = FastGraph()
        g.add_Node(sn1)

        g.add_Decomp(sn1, dn1)

        g.add_Node(sn11)


        fig = plt.figure(figsize=(10, 30))
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        g.draw_matplotlib(ax1)
        G, new_set = add_combis_arg_set_graphs_to_decomp(
            g,
            dn1,
            frozenset({
                frozenset({tC.a3_from_b0, tC.b1_from_a2}),
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        G.draw_matplotlib(ax2)

        G_ref=deepcopy(g)
        G_ref.add_edge(
            sn11,
            dn1,
            computer_sets=frozenset({
                frozenset({tC.a3_from_b0, tC.b1_from_a2}),
                frozenset({tC.a3_from_a2, tC.b1_from_b0})
            })
        )
        G_ref.draw_matplotlib(ax3)
        fig.savefig("figure.pdf")
        self.assertEqual(G, G_ref)
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
        g = FastGraph()
        g.add_Node(sn1)

        g.add_Decomp(sn1, dn1) 

        #g.add_node(sn11, bipartite=0) # unneccessary because sn11 is a superset of sn12, sn13


        fig = plt.figure(figsize=(30, 10))
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        g.draw_matplotlib(ax1)
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
        g_res.draw_matplotlib(ax2)

        G_ref=deepcopy(g)
        G_ref.add_Node(sn12)
        G_ref.add_Node(sn13)
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
        G_ref.draw_matplotlib(ax3)
        fig.savefig("figure.pdf")
        self.assertEqual(g_res, G_ref)
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
        g = FastGraph()
        g.add_Node(sn1)

        g.add_Decomp(sn1,dn1)

        #g.add_node(sn11, bipartite=0)


        fig = plt.figure(figsize=(30, 10))
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        g.draw_matplotlib(ax1)
        
        G_ref=deepcopy(g)
        G_ref.add_Node(sn12)
        G_ref.add_Node(sn13)
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
        G_ref.draw_matplotlib(ax2)



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
        g_res.draw_matplotlib(ax3)

        fig.savefig("figure.pdf")
        self.assertEqual(g_res, G_ref)
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
        g_base = FastGraph()
        g_base.add_Node(sn1)

        g_base.add_Decomp(sn1, dn1)
        g_base.add_Decomp(sn1, dn2)
        g_base.add_Decomp(sn1, dn3)
        
        g_ref = deepcopy(g_base)
        sn111 = frozenset([A2])
        g_ref.add_Node(sn111)
        g_ref.add_edge(
            sn111,
            dn1,
            computer_sets = frozenset([
                frozenset({tC.a3_from_a2, tC.b1_from_a2})
            ])
        )
        sn112 = frozenset([B0])
        g_ref.add_Node(sn112)
        g_ref.add_edge(
            sn112,
            dn1,
            computer_sets = frozenset([
                frozenset({tC.a3_from_b0, tC.b1_from_b0})
            ])
        )
        sn121 = frozenset([A2, B1])
        g_ref.add_Node(sn121)
        g_ref.add_edge(
            sn121,
            dn2,
            computer_sets = frozenset([
                frozenset({tC.a3_from_a2})
            ])
        )
        sn122 = frozenset([B0, B1])
        g_ref.add_Node(sn122)
        g_ref.add_edge(
            sn122,
            dn2,
            computer_sets = frozenset([
                frozenset({tC.a3_from_b0})
            ])
        )
        sn131 = frozenset([A3, B0])
        g_ref.add_Node(sn131)
        g_ref.add_edge(
            sn131,
            dn3,
            computer_sets = frozenset([
                frozenset({tC.b1_from_b0})
            ])
        )
        sn132 = frozenset([A3, A2])
        g_ref.add_Node(sn132)
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
        g_base.draw_matplotlib(ax1)
        g_ref.draw_matplotlib(ax2)
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
        g_res.draw_matplotlib(ax3)
        fig.savefig("figure.pdf")
        self.assertEqual(g_ref, g_res)
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
        g_base = FastGraph()
        # var set
        sn1 = frozenset([A, B, C])
        g_base.add_Node(sn1)
        
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
            g_ref.add_Decomp(sn1, dn)


        fig = plt.figure(figsize=(30, 20))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        
        g_ref.draw_matplotlib(ax1)

        uncomputable = frozenset([])
        g = deepcopy(g_base)
        g_res, new_decompositions = fgh.add_all_decompositions_to_node(g, sn1, uncomputable)
        g_res.draw_matplotlib(ax2)

        fig.savefig("figure.pdf")
        self.assertEqual(
            g_ref,
            g_res
        )
        print(frozenset.difference(new_decompositions, decompositions))
        print(frozenset.difference(decompositions, new_decompositions))
        self.assertEqual(
            decompositions,
            new_decompositions
        )

    def test_add_all_decompositions_to_node_with_uncomputables(self):
        g_base = FastGraph()
        # var set
        sn1 = frozenset([A, B, C])
        g_base.add_Node(sn1)
        
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
            g_ref.add_Decomp(sn1,dn) 


        fig = plt.figure(figsize=(30, 20))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        
        g_ref.draw_matplotlib(
            ax1,
        )
        uncomputable = frozenset([C])
        g = deepcopy(g_base)
        g_res, new_decompositions = fgh.add_all_decompositions_to_node(g, sn1, uncomputable)
        g_res.draw_matplotlib(
            ax2,
        )
        fig.savefig("figure.pdf")
        self.assertEqual(
            g_ref,
            g_res
        )
        print(frozenset.difference(new_decompositions, decompositions))
        print(frozenset.difference(decompositions, new_decompositions))
        self.assertEqual(
            decompositions,
            new_decompositions
        )


    def test_initial_fast_graph(self):
        computers = self.computers
        g = FastGraph()
        for v in [A, B, C, D, E, F, G, H, I, J]:
            g.add_Node(frozenset([v]))

        new_decompositions = frozenset(
            [
                (frozenset([v]), frozenset([])) 
                for v in [A, B, J]
            ]
        )
        for dn in new_decompositions: 
            g.add_Decomp(dn[0],dn)

        g_res,new_decompositions_res  = fgh.initial_fast_graph(computers)
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        g.draw_matplotlib(ax1)
        
        g_res.draw_matplotlib(ax2)

        fig.savefig("figure.pdf")

        self.assertEqual(g_res, g)
        self.assertTrue(
            new_decompositions,
            new_decompositions_res
        )

    def test_manual_sequence(self):
        computers = frozenset({
            tC.b_from_c_d,
            tC.d_from_a
        })
        #g = FastGraph()
        #for v in [A, B, C, D]:
        #    g.add_Node(frozenset([v]))

        #new_decompositions = frozenset(
        #    [
        #        (frozenset([v]), frozenset([])) 
        #        for v in [B, D]
        #    ]
        #)
        #for dn in new_decompositions: 
        #    g.add_Decomp(dn[0],dn)
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(6, 1, 1)
        ax2 = fig.add_subplot(6, 1, 2)
        ax3 = fig.add_subplot(6, 1, 3)
        ax4 = fig.add_subplot(6, 1, 4)
        ax5 = fig.add_subplot(6, 1, 5)
        ax6 = fig.add_subplot(6, 1, 6)

        g_res1,decompositions1 = fgh.initial_fast_graph(computers)
        g_res1.draw_matplotlib(ax1)
        pp('decompositions1',locals())

        g_res2,nodes2 = fgh.add_arg_set_graphs_to_decomps(
            g_res1,
            decompositions1,
            computers
        )
        g_res2.draw_matplotlib(ax2)
        pp('nodes2',locals())

        uncomputable=h.uncomputable(computers)
        #pp('uncomputable',locals())
        g_res3,decompositions3= fgh.add_all_decompositions_to_all_nodes(
            g_res2,
            nodes2,
            uncomputable=uncomputable
        )
        g_res3.draw_matplotlib(ax3)
        pp('decompositions3',locals())
        
        g_res4,nodes4 = fgh.add_arg_set_graphs_to_decomps(
            g_res3,
            decompositions3,
            computers
        )
        g_res4.draw_matplotlib(ax4)
        pp('nodes4',locals())

        g_res5,decompositions5 = fgh.add_all_decompositions_to_all_nodes(
            g_res4,
            nodes4,
            uncomputable=uncomputable
        )
        g_res5.draw_matplotlib(ax5)
        pp('decompositions5',locals())

        g_res6,nodes6 = fgh.add_arg_set_graphs_to_decomps(
            g_res5,
            decompositions5,
            computers
        )
        g_res6.draw_matplotlib(ax6)
        pp('nodes6',locals())
        fig.savefig("figure.pdf")

        
    def test_add_all_decompositions_to_all_nodes(self):
        g = FastGraph() 
        n1 = frozenset([tC.A, tC.B])
        n2 = frozenset([tC.J])
        g.add_Node(n1)
        g.add_Node(n2)
        
        uncomputable = h.uncomputable(self.computers)
        g_res, new_decompositions = fgh.add_all_decompositions_to_all_nodes(
            g, 
            nodes=frozenset([n1, n2]),
            uncomputable=uncomputable
        )
        fig = plt.figure(figsize=(30, 20))
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)

        g.draw_matplotlib(ax1)
        
        g_res.draw_matplotlib(ax3)
        
        fig.savefig("figure.pdf")
        
        
    def test_update_generator(self):
        # this will draw the update sequence
        computers = frozenset({
            tC.b_from_c_d,
            tC.d_from_a
        })
        max_it = 10
        graphs = [graph  for (graph, new) in fgh.update_generator(computers,max_it=max_it)]
        fig = plt.figure(figsize=(40, 20))
        fgh.draw_update_sequence(
            computers,
            max_it=max_it,
            fig=fig
        )   
        fig.savefig("figure.pdf")


    def test_fast_graph(self):
        computers = self.computers
        g = FastGraph()
        for v in [A, B, C, D, E, F, G, H, I, J]:
            g.add_Node(frozenset({v}))

        new_decompositions = frozenset(
            [
                (frozenset([v]), frozenset([])) 
                for v in [A, B, J]
            ]
        )
        for dn in new_decompositions: 
            g.add_Decomp(dn[0], dn)

        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        g.draw_matplotlib(ax1)
        #from IPython import embed; embed()
        g_res = fgh.fast_graph(computers)
        g_res.draw_matplotlib(ax2)
        fig.savefig("figure.pdf")
        
