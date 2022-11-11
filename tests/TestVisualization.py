#!/usr/bin/env python3
import matplotlib.pyplot as plt
from copy import  deepcopy
from bokeh.io import output_file, show, output_notebook
from testinfrastructure.InDirTest import InDirTest
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
    draw_ComputerSetMultiDiGraph_matplotlib,
    bokeh_plot
)
from ComputabilityGraphs.FastGraph import FastGraph
import ComputabilityGraphs.helpers as h
from ComputabilityGraphs.Node import Node
from ComputabilityGraphs.Decomposition import Decomposition
from ComputabilityGraphs.ComputerSet import ComputerSet
from ComputabilityGraphs.ComputerSetSet import ComputerSetSet

from testComputers import (
    A, A2, A3, B, B1, B0, C, D, E, F, G, H, I,
    a_from_i,
    b_from_c_d,
    b_from_e_f,
    c_from_b,
    d_from_b,
    d_from_g_h,
    a3_from_a2,
    b1_from_b0,
    a3_from_b0,
    b1_from_a2,
    e_from_b,
    f_from_b,
)
# from testComputers import computers
import testComputers as tC
from unittest import skip

class TestVisualization(InDirTest):
    def setUp(self):
        self.computers = tC.computers


    @skip
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
        #G=nx.DiGraph()
        #G.add_edges_from([("A",n) for n in ("B","C","D","E","F")])
        plot=bokeh_plot(G)
        show(plot)
        #output_notebook()
        #output_file("graph.html")

#    
    @skip
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
                cs=computers,
                given=frozenset()
            )
        )
        
        res_A = minimal_startnodes_for_single_var(fspsg_A, A)
        ### target B
        fspsg_B = fgh.project_to_multiDiGraph(
            fgh.fast_graph(
                root_type=B,
                cs=computers,
                given=frozenset()
            )
        )
        res_B = minimal_startnodes_for_single_var(fspsg_B, B)
        ### target C
        fspsg_C = fgh.project_to_multiDiGraph(
            fgh.fast_graph(
                root_type=C,
                cs=computers,
                given=frozenset()
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
