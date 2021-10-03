#!/usr/bin/env python3
from typing import FrozenSet
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
from ComputabilityGraphs.graph_helpers import (
        minimal_startnodes_for_single_var,
)
import ComputabilityGraphs.fast_graph_helpers as fgh
from ComputabilityGraphs.graph_plotting import (
    draw_ComputerSetMultiDiGraph_matplotlib
)
from ComputabilityGraphs.FastGraph import FastGraph
import ComputabilityGraphs.helpers as h
from ComputabilityGraphs.Node import Node
from ComputabilityGraphs.Decomposition import Decomposition
from ComputabilityGraphs.ComputerSet import ComputerSet
from ComputabilityGraphs.ComputerSetSet import ComputerSetSet

from testComputers import (
    A, A1, A2, A3, A0, A_minus_1, A_minus_2, B,
    B1, B2, B3, B0, B_minus_1, B_minus_2, C, D, E, F, G, H, I,J, X, Y,
    a_from_x,
    b_from_y,
    a_from_i,
    b_from_c_d,
    b_from_e_f,
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
    a0_from_b0,
    a3_from_b0,
    b1_from_a2,
    e_from_b,
    f_from_b,
)
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

    def test_src_node_computersets_tuples_from_decomp(self):
        # var set
        sn = frozenset([A3, B1])
        sn10 = frozenset([A2, B1])
        sn11 = frozenset([B0, B1])
        dn1 = (
            frozenset([A3]),        # active
            frozenset([B1])         # pass
        )
        css10 = frozenset({
            frozenset({tC.a3_from_a2})
        })
        css11 = frozenset({
            frozenset({tC.a3_from_b0}),
        })
        g = FastGraph()
        g.add_Node(sn)

        g.add_Decomp(sn,dn1)
        g.add_Node(sn10)
        g.add_Node(sn11)
        g.add_edge(
            sn10,
            dn1,
            computer_sets=css10
        )
        g.add_edge(
            sn11,
            dn1,
            computer_sets=css11
        )
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 1, 1)
        
        g.draw_matplotlib(ax)

        fig.savefig("figure.pdf")
        
        res = fgh.src_node_computersets_tuples_from_decomp(g,dn1)

        self.assertEqual(
            res,
            frozenset([
                (sn10,css10) ,(sn11,css11)
            ])
        ) 



    def test_src_node_computersets_tuples_from_node(self):
        # node
        sn = frozenset([A3, B1])
        # decomp
        dn0 = (
            frozenset([A3,B1]),        # active
            frozenset()                # pass
        )
        sn00 = frozenset([A2, B0])
        css00 = frozenset([
            frozenset({tC.a3_from_a2, tC.b1_from_b0}),
            frozenset({tC.a3_from_b0, tC.b1_from_a2})
        ])
        tn00 = (sn00, css00)

        sn01 = frozenset([A2])
        css01 = frozenset([
            frozenset({tC.a3_from_a2, tC.b1_from_a2})
        ])
        tn01 = (sn01, css01)


        sn02 = frozenset([B0])
        css02 = frozenset([
            frozenset({tC.a3_from_b0, tC.b1_from_b0})
        ])
        tn02 = (sn02, css02)
        
        dn1 = (
            frozenset([A3]),        # active
            frozenset([B1])         # pass
        )
        sn10 = frozenset([A2, B1])
        css10 = frozenset({
            frozenset({tC.a3_from_a2})
        })
        tn10 = (sn10,css10)

        sn11 = frozenset([B0, B1])
        css11 = frozenset({
            frozenset({tC.a3_from_b0}),
        })
        tn11 = (sn11,css11)

        g = FastGraph()
        g.add_Node(sn)
        g.add_Decomp(sn,dn0)
        g.add_Node(sn00)
        g.add_edge(
            sn00,
            dn0,
            computer_sets=css00
        )
        g.add_Node(sn01)
        g.add_edge(
            sn01,
            dn0,
            computer_sets=css01
        )
        g.add_Node(sn02)
        g.add_edge(
            sn02,
            dn0,
            computer_sets=css02
        )

        g.add_Decomp(sn,dn1)
        g.add_Node(sn10)
        g.add_Node(sn11)
        g.add_edge(
            sn10,
            dn1,
            computer_sets=css10
        )
        g.add_edge(
            sn11,
            dn1,
            computer_sets=css11
        )
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 1, 1)
        
        g.draw_matplotlib(ax)

        fig.savefig("figure.pdf")
        res = fgh.src_node_computersets_tuples_from_node(g,sn)
        
        self.assertEqual(
            res,
            frozenset([
               tn00,
               tn01,
               tn02,
               tn10,
               tn11
            ])
        ) 

    def test_nodes_on_paths(self):
        g = FastGraph()
        n0 = Node({B})
        g.add_Node(n0)
        d0a = Decomposition(
            active=n0,
            passive=Node()
        )
        g.add_Decomp(
            decomp=d0a,
            targetNode=n0
        )
        n0a0 = Node({C,D})
        g.add_connected_Node(
            node=n0a0,
            target_decomp=d0a,
            computer_sets=ComputerSetSet({
                ComputerSet({b_from_c_d})
            })
        )
        d0a0a = Decomposition(
            active=Node({D}),
            passive=Node({C})
        )
        g.add_Decomp(
            decomp=d0a0a,
            targetNode=n0a0
        )
        n0a0a0 = Node({C,G,H})
        g.add_connected_Node(
            node=n0a0a0,
            target_decomp=d0a0a,
            computer_sets=ComputerSetSet({
                ComputerSet({d_from_g_h})
            })
        )

        fig = plt.figure(figsize=(10, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        g.draw_matplotlib(ax1)
        fig.savefig("figure.pdf")

        res_p = g.passive_Nodes_in_Decompositions_on_paths(
            src=n0a0a0,
            root=n0
        )
        self.assertEqual(
            res_p,
            frozenset({Node({}),Node({C})})
        )
        # now we check for the Nodes on the 
        # path to the root (this is important
        # to check before adding a new src_Node 
        res_n = g.visited_Nodes_on_paths(
            src=d0a0a,
            root=n0
        )
        self.assertEqual(
            res_n,
            frozenset({Node({B}),Node({C,D})})
        )


    def test_project(self):
        # project the bipartite graph consisting of two kinds of nodes (sets
        # and decompositions) to the graph we actually need which has only sets
        # The aim is to retain the edge information (The sets of computersets
        # that connect the sets of variables)
        # node
        sn = frozenset([A3, B1])
        # decomp
        dn0 = (
            frozenset([A3,B1]),        # active
            frozenset()                # pass
        )
        sn00 = frozenset([A2, B0])
        css00 = frozenset([
            frozenset({tC.a3_from_a2, tC.b1_from_b0}),
            frozenset({tC.a3_from_b0, tC.b1_from_a2})
        ])
        tn00 = (sn00, css00)

        sn01 = frozenset([A2])
        css01 = frozenset([
            frozenset({tC.a3_from_a2, tC.b1_from_a2})
        ])
        tn01 = (sn01, css01)


        sn02 = frozenset([B0])
        css02 = frozenset([
            frozenset({tC.a3_from_b0, tC.b1_from_b0})
        ])
        tn02 = (sn02, css02)
        
        dn1 = (
            frozenset([A3]),        # active
            frozenset([B1])         # pass
        )
        sn10 = frozenset([A2, B1])
        css10 = frozenset({
            frozenset({tC.a3_from_a2})
        })
        tn10 = (sn10,css10)

        sn11 = frozenset([B0, B1])
        css11 = frozenset({
            frozenset({tC.a3_from_b0}),
        })
        tn11 = (sn11,css11)

        g = FastGraph()
        g.add_Node(sn)
        g.add_Decomp(sn,dn0)
        g.add_Node(sn00)
        g.add_edge(
            sn00,
            dn0,
            computer_sets=css00
        )
        g.add_Node(sn01)
        g.add_edge(
            sn01,
            dn0,
            computer_sets=css01
        )
        g.add_Node(sn02)
        g.add_edge(
            sn02,
            dn0,
            computer_sets=css02
        )

        g.add_Decomp(sn,dn1)
        g.add_Node(sn10)
        g.add_Node(sn11)
        g.add_edge(
            sn10,
            dn1,
            computer_sets=css10
        )
        g.add_edge(
            sn11,
            dn1,
            computer_sets=css11
        )

        fig = plt.figure(figsize=(10, 20))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        g.draw_matplotlib(ax1)

        fig.savefig("figure.pdf")

        G = fgh.project_to_multiDiGraph(g)
    
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
            root=sn1,
            decomp=dn1,
            computer_combi=ComputerSet({tC.a3_from_a2, tC.b1_from_b0})
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
            root=sn1,
            decomp=dn1,
            computer_combi=ComputerSet({tC.a3_from_a2, tC.b1_from_b0})
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
            root=sn1,
            decomp=dn1,
            computer_combi=ComputerSet({tC.a3_from_b0, tC.b1_from_a2})
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
            root=sn1,
            decomp=dn1,
            computer_combis=ComputerSetSet({
                ComputerSet({tC.a3_from_b0, tC.b1_from_a2}),
                ComputerSet({tC.a3_from_a2, tC.b1_from_b0})
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
        computers = ComputerSet([
            a3_from_a2,
            a3_from_b0,
            b1_from_b0,
            b1_from_a2
        ])
        g_res, new_set = add_all_arg_set_graphs_to_decomp(
            g,
            root=sn1,
            decomp=dn1,
            all_computers=computers
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



        computers = ComputerSet([
            a3_from_a2,
            a3_from_b0,
            b1_from_b0,
            b1_from_a2
        ])
        
        g_res, new_set = add_all_arg_set_graphs_to_decomp(
            g,
            root=sn1,
            decomp=dn1,
            all_computers=computers
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
            root=sn1,
            decomps=frozenset([dn1, dn2, dn3]),
            all_computers=computers
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
        sn1 = Node([A, B, C])
        g_base.add_Node(sn1)
        
        g_ref = deepcopy(g_base)
        # decompositions
        decompositions = frozenset([
            (
                Node([A, B, C]),    # active
                Node([])           # passive
            ),
            (
                Node([A, B]),    # active
                Node([C])           # passive
            ),
            (
                Node([C]),    # active
                Node([A, B])           # passive
            ),
            (
                Node([A, C]),    # active
                Node([B])           # passive
            ),
            (
                Node([B]),    # active
                Node([A,C])           # passive
            ),
            (
                Node([B, C]),    # active
                Node([A])           # passive
            ),
            (
                Node([A]),    # active
                Node([B,C])           # passive
            ),
            # the following decomposition is never relevant
            # since it reproduces its origin (by keeping it passive)
            # so the algorithm discards it automatically
            #(
            #    Node([]),    # active
            #    Node([A, B, C])           # passive
            #)
        ])

        for dn in decompositions:
            g_ref.add_Decomp(sn1, dn)


        fig = plt.figure(figsize=(20, 30))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        
        g_ref.draw_matplotlib(ax1)

        uncomputable = frozenset()
        g = deepcopy(g_base)
        g_res, new_decompositions = fgh.add_all_decompositions_to_node(g, sn1, uncomputable)
        g_res.draw_matplotlib(ax2)

        fig.savefig("figure.pdf")
        self.assertEqual(
            g_res,
            g_ref
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
            # the following decomposition is never relevant
            # since it reproduces its origin (by keeping it passive)
            # so the algorithm discards it automatically
            #(
            #    frozenset([]),    # active
            #    frozenset([A, B, C])           # passive
            #)
        ])

        for dn in decompositions:
            g_ref.add_Decomp(sn1,dn) 


        fig = plt.figure(figsize=(30, 20))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        
        g_ref.draw_matplotlib(
            ax1,
        )
        passive= frozenset([ Node([C]) ])
        g = deepcopy(g_base)
        g_res, new_decompositions = fgh.add_all_decompositions_to_node(
                g, 
                sn1, 
                passive=passive)
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
        n = Node([B])
        g.add_Node(n)
        d = Decomposition(
            active=n, 
            passive=Node([])
        ) 
        g.add_Decomp(decomp=d,targetNode=n)
        new_decompositions = frozenset([d])

        g_res,new_decompositions_res  = fgh.initial_fast_graph(
                                            root_type=B,
                                            cs=computers
                                        )
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

        g_res1, decompositions1 = fgh.initial_fast_graph(
                                    root_type=B,
                                    cs=computers
                                )
        root=Node({B})
        g_res1.draw_matplotlib(ax1)
        pp('decompositions1',locals())

        g_res2,nodes2 = fgh.add_arg_set_graphs_to_decomps(
            g_res1,
            root=root,
            decomps=decompositions1,
            all_computers=computers
        )
        g_res2.draw_matplotlib(ax2)
        pp('nodes2',locals())

        uncomputable=h.uncomputable(computers)
        #pp('uncomputable',locals())
        g_res3,decompositions3= fgh.add_all_decompositions_to_all_nodes(
            g_res2,
            root=root,
            nodes=nodes2,
            uncomputable=uncomputable
        )
        g_res3.draw_matplotlib(ax3)
        pp('decompositions3',locals())
        
        g_res4,nodes4 = fgh.add_arg_set_graphs_to_decomps(
            g_res3,
            root=root,
            decomps=decompositions3,
            all_computers=computers
        )
        g_res4.draw_matplotlib(ax4)
        pp('nodes4',locals())

        g_res5,decompositions5 = fgh.add_all_decompositions_to_all_nodes(
            g_res4,
            root=root,
            nodes=nodes4,
            uncomputable=uncomputable
        )
        g_res5.draw_matplotlib(ax5)
        pp('decompositions5',locals())

        g_res6,nodes6 = fgh.add_arg_set_graphs_to_decomps(
            g_res5,
            root=root,
            decomps=decompositions5,
            all_computers=computers
        )
        g_res6.draw_matplotlib(ax6)
        pp('nodes6',locals())
        fig.savefig("figure.pdf")

        
    def test_add_all_decompositions_to_all_nodes(self):
        g = FastGraph() 
        n1 = frozenset([tC.A, tC.B])
        n2 = frozenset([tC.J])
        g.add_Node(n1)
        
        uncomputable = h.uncomputable(self.computers)
        g_res, new_decompositions = fgh.add_all_decompositions_to_all_nodes(
            g, 
            root=n1,
            nodes=frozenset([n1]),
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
            a_from_i,
            c_from_b,
            b_from_c_d,
            d_from_g_h
        })
        max_it = 10
        graphs = [graph  for (graph, new) in fgh.update_generator(
            root_type=B,
            cs=computers,
            max_it=max_it
        )]
        fig = plt.figure(figsize=(40, 20))
        fgh.draw_update_sequence(
            root_type=B,
            computers=computers,
            max_it=max_it,
            fig=fig
        )   
        fig.savefig("figure.pdf")


    def test_to_Agraph(self):
        computers = self.computers
        fig = plt.figure(figsize=(10, 20))
        ax1 = fig.add_subplot(1, 1, 1)
        g_res = fgh.fast_graph(
                root_type=C,
                cs=computers
        )
        g_res.draw_matplotlib(ax1)
        fig.savefig("figure.pdf")
        A=g_res.to_AGraph()
        A.layout("neato")
        A.draw('A.ps') 
    
class TestFastGraph3(InDirTest):
    def test_minimal_startnodes_for_single_var(self):
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
                b_from_e_f,
                c_from_b,
                d_from_b,
                d_from_g_h,
                e_from_b,
                f_from_b,
            ]
        )
        ## target A
        fspsg_A = fgh.project_to_multiDiGraph(
            fgh.fast_graph(
                        root_type=A,
                        cs=computers
                )
        )
        
        res_A = minimal_startnodes_for_single_var(fspsg_A, A)
        ### target B
        fspsg_B = fgh.project_to_multiDiGraph(
            fgh.fast_graph(
                        root_type=B,
                        cs=computers
                )
        )
        res_B = minimal_startnodes_for_single_var(fspsg_B, B)
        ### target C
        fspsg_C = fgh.project_to_multiDiGraph(
            fgh.fast_graph(
                        root_type=C,
                        cs=computers
                )
        )
        res_C = minimal_startnodes_for_single_var(fspsg_C, C)
        
        # plot
        fig = plt.figure(figsize=(15, 45))
        axs = fig.subplots(3, 1)
        draw_ComputerSetMultiDiGraph_matplotlib(
            axs[0],
            fspsg_A,
            targetNode=Node({A})
        )
        draw_ComputerSetMultiDiGraph_matplotlib(
            axs[1],
            fspsg_B,
            targetNode=Node({B})
        )
        draw_ComputerSetMultiDiGraph_matplotlib(
            axs[2],
            fspsg_C,
            targetNode=Node({C})
        )
        fig.savefig("figure.pdf")



        # assertions
        self.assertSetEqual(
            res_A,
            frozenset({
                Node({I})
            })
        )
        self.assertSetEqual(
            res_B,
            frozenset({
                frozenset({E, F}),
                frozenset({C, D}),
                frozenset({H, C, G})
            })
        )
        self.assertSetEqual(
            res_C,
            frozenset({
                frozenset({E, F}),
                frozenset({B})
            })
        )
