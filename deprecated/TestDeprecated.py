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
    arg_set_graph,
    initial_sparse_powerset_graph,
    minimal_startnodes_for_single_var,
    minimal_startnodes_for_node,
    update_step,
    toDiGraph,
    equivalent_multigraphs,
    product_graph,
    sparse_powerset_graph,
    fast_sparse_powerset_graph,
    update_generator,
    # draw_multigraph_plotly,
    # draw_Graph_svg,
)

from ComputabilityGraphs.graph_plotting import (
    draw_update_sequence,
    draw_ComputerSetDiGraph_matplotlib,
    draw_ComputerSetMultiDiGraph_matplotlib,
)
from ComputabilityGraphs.helpers import (
    arg_set_set,
    all_mvars, 
    node_2_string,
    nodes_2_string,
    edge_2_string,
    equivalent_singlegraphs,
)



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
    a0_from_b0,
    a_from_i,
    b_from_c_d,
    b_from_e_f,
    c_from_b,
    d_from_b,
    d_from_g_h,
    e_from_b,
    f_from_b,
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

    def test_arg_set_graph(self):
        asg = arg_set_graph(D, self.computers)
        # For compatibility arg_set_graph returns a multigraph
        # although we do not have more than one edge between a pair
        # of nodes.

        ref = nx.MultiDiGraph()
        ref.add_edge(
            frozenset({B}),
            frozenset({D}),
            computers=frozenset({d_from_b})
        )
        ref.add_edge(
            frozenset({G, H}),
            frozenset({D}),
            computers=frozenset({d_from_g_h})
        )

        # picture for manual check
        fig = plt.figure(figsize=(20, 20))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        draw_ComputerSetMultiDiGraph_matplotlib(ax1, ref)
        draw_ComputerSetMultiDiGraph_matplotlib(ax2, asg)
        fig.savefig("arg_set_graph.pdf")

        self.assertTrue(equivalent_multigraphs(asg, ref))

    def test_product_graph(self):
        computers = frozenset({a_from_y, a_from_z, b_from_y, b_from_z})

        asg_A = arg_set_graph(A, computers)
        asg_B = arg_set_graph(B, computers)
        pg_A_B = product_graph(asg_A, asg_B)

        fig1 = plt.figure(figsize=(20, 100))

        ax1 = fig1.add_subplot(411, frame_on=True, title="arg_set_graph(A)")
        ax2 = fig1.add_subplot(412, frame_on=True, title="arg_set_graph(B)")
        ax3 = fig1.add_subplot(413, frame_on=True, title="product_graph(A,B)")
        # ax4=fig1.add_subplot(414,frame_on=True,title="ref")
        draw_ComputerSetMultiDiGraph_matplotlib(ax1, asg_A)
        draw_ComputerSetMultiDiGraph_matplotlib(ax2, asg_B)
        draw_ComputerSetMultiDiGraph_matplotlib(ax3, pg_A_B)
        fig1.savefig("AB_Z.pdf")

        computers = frozenset({a_from_y, b_from_y, b_from_z})
        asg_A = arg_set_graph(A, computers)
        asg_B = arg_set_graph(B, computers)
        pg_A_B = product_graph(asg_A, asg_B)

        fig1 = plt.figure(figsize=(10, 30))
        ax1 = fig1.add_subplot(411, frame_on=True, title="arg_set_graph(A)")
        ax2 = fig1.add_subplot(412, frame_on=True, title="arg_set_graph(B)")
        ax3 = fig1.add_subplot(413, frame_on=True, title="product_graph(A,B)")
        # ax4=fig1.add_subplot(414,frame_on=True,title="ref")
        draw_ComputerSetMultiDiGraph_matplotlib(ax1, asg_A)
        draw_ComputerSetMultiDiGraph_matplotlib(ax2, asg_B)
        draw_ComputerSetMultiDiGraph_matplotlib(ax3, pg_A_B)
        fig1.savefig("A_y_B_Y_B_Z.pdf")

        #    {a(z)}          {b(z)}          {a(z),b(z)}

        # {z}  ->  {a} x {z}  ->   {b}   = {z} -> {a,b}

        computers = frozenset({a_from_z, b_from_z})
        asg_A = arg_set_graph(A, computers)
        asg_B = arg_set_graph(B, computers)
        pg_A_B = product_graph(asg_A, asg_B)

        fig1 = plt.figure(figsize=(10, 30))
        ax1 = fig1.add_subplot(411, frame_on=True, title="arg_set_graph(A)")
        ax2 = fig1.add_subplot(412, frame_on=True, title="arg_set_graph(B)")
        ax3 = fig1.add_subplot(413, frame_on=True, title="product_graph(A,B)")
        # ax4=fig1.add_subplot(414,frame_on=True,title="ref")
        draw_ComputerSetMultiDiGraph_matplotlib(ax1, asg_A)
        draw_ComputerSetMultiDiGraph_matplotlib(ax2, asg_B)
        draw_ComputerSetMultiDiGraph_matplotlib(ax3, pg_A_B)
        fig1.savefig("A_Z_B_Y.pdf")

        computers = frozenset({a_from_z, b_from_z, c_from_b})
        asg_A = arg_set_graph(A, computers)
        asg_B = arg_set_graph(B, computers)
        asg_C = arg_set_graph(C, computers)
        asg_C = arg_set_graph(C, computers)
        prod = product_graph(*[asg_A, asg_B, asg_C])

        fig1 = plt.figure(figsize=(10, 30))
        ax1 = fig1.add_subplot(511, frame_on=True, title="arg_set_graph(A)")
        ax2 = fig1.add_subplot(512, frame_on=True, title="arg_set_graph(B)")
        ax3 = fig1.add_subplot(513, frame_on=True, title="arg_set_graph(C)")
        ax4 = fig1.add_subplot(514, frame_on=True, title="product_graph(A,B,C)")
        # ax4=fig1.add_subplot(414,frame_on=True,title="ref")
        draw_ComputerSetMultiDiGraph_matplotlib(ax1, asg_A)
        draw_ComputerSetMultiDiGraph_matplotlib(ax2, asg_B)
        draw_ComputerSetMultiDiGraph_matplotlib(ax3, asg_C)
        draw_ComputerSetMultiDiGraph_matplotlib(ax4, prod)
        fig1.savefig("ABC.pdf")

    def test_Markus_graph_creation(self):
        # Now we build the directed Graph we can use to compute connectivity
        # the Nodes are sets of Mvars (elemenst of the powerset of all Mvars)
        # and a connection between two sets indicates computability of the target set from
        # the source set.
        # The complete graph would contain all elements of the powerset of allMvars and all
        # possible connections, which is prohibitively expensive.
        # Instead we will compute a tree where we start with a single one element sets a target
        # and infer the predecessors and then the predecessors of the predecessors and so on until 
        # we do not find new nodes=start_sets.
        # spsg=sparse_powerset_graph(self.mvars,self.computers)

        ################# linear A1->A2->A3
        computers = frozenset({a2_from_a1, a3_from_a2})
        spsg = sparse_powerset_graph(computers)
        
        self.assertSetEqual(
            set(spsg.nodes()), {frozenset({A1}), frozenset({A2}), frozenset({A3})}
        )
        self.assertSetEqual(
            set(spsg.edges()),
            {(frozenset({A1}), frozenset({A2})), (frozenset({A2}), frozenset({A3}))},
        )
        ################## cross
        #       B-2->B-1->B0->B1->B2
        #                  ||
        #                  \/
        #       A-2->A-1->A0->A1->A2
        computers = frozenset(
            {
                b_minus_1_from_b_minus_2,
                b0_from_b_minus_1,
                b1_from_b0,
                b2_from_b1,
                b3_from_b2,
                #
                a0_from_b0,
                #
                a_minus_1_from_a_minus_2,
                a0_from_a_minus_1,
                a1_from_a0,
                a2_from_a1,
                a3_from_a2,
            }
        )
        spsg = sparse_powerset_graph(computers)
        self.assertSetEqual(
            set(spsg.nodes()),
            {
                frozenset({B_minus_1}),
                frozenset({B_minus_2}),
                frozenset({B0}),
                frozenset({B1}),
                frozenset({B2}),
                frozenset({B3}),
                frozenset({A_minus_1}),
                frozenset({A_minus_2}),
                frozenset({A0}),
                frozenset({A1}),
                frozenset({A2}),
                frozenset({A3}),
            },
        )
        self.assertSetEqual(
            set(spsg.edges()),
            {
                (frozenset({B_minus_2}), frozenset({B_minus_1})),
                (frozenset({B_minus_1}), frozenset({B0})),
                (frozenset({B0}), frozenset({B1})),
                (frozenset({B1}), frozenset({B2})),
                (frozenset({B2}), frozenset({B3})),
                #
                (frozenset({B0}), frozenset({A0})),
                #
                (frozenset({A_minus_2}), frozenset({A_minus_1})),
                (frozenset({A_minus_1}), frozenset({A0})),
                (frozenset({A0}), frozenset({A1})),
                (frozenset({A1}), frozenset({A2})),
                (frozenset({A2}), frozenset({A3})),
            },
        )

    def test_Markus_graph_creation2(self):
        #check difference
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
                #b_from_e_f,
                c_from_b,
                #d_from_b,
                d_from_g_h,
                #e_from_b,
                #f_from_b,
            ]
        )
        fig=plt.figure()
        draw_update_sequence(computers,5,fig)
        fig.savefig('update.pdf')
        

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
        spsg = sparse_powerset_graph(self.computers)
        fig1 = plt.figure(figsize=(15, 15))
        axs = fig1.subplots(2, 1)
        draw_ComputerSetMultiDiGraph_matplotlib(
            axs[0],
            spsg,
            targetNode=frozenset({B})
        )

        fig1.savefig("spsg_B.pdf")
        plt.close(fig1)
        # After the graph has been computed we can use it
        # to infer computability of all Mvars
        res_B = minimal_startnodes_for_single_var(spsg, B)
        self.assertSetEqual(
            res_B,
            frozenset({
                frozenset({E, F}),
                frozenset({C, D}),
                frozenset({H, C, G}),
                frozenset({H, C, D, G}),
                frozenset({E, H, F, G})
            })
        )
        fig1 = plt.figure(figsize=(15, 15))
        axs = fig1.subplots(1, 1)
        draw_ComputerSetMultiDiGraph_matplotlib(
            axs,
            spsg,
            targetNode=frozenset({A})
        )
        fig1.savefig("spsg_A.pdf")
        plt.close(fig1)
        res_A = minimal_startnodes_for_single_var(spsg, A)
        self.assertSetEqual(
            res_A,
            frozenset({
                frozenset({I})
            })
        )

    def test_minimal_startnodes_for_node(self):
        spsg = sparse_powerset_graph(self.computers)
        targetVars = frozenset({A, B})
        fig1 = plt.figure(figsize=(15, 30))
        axs = fig1.subplots(2, 1)
        draw_ComputerSetMultiDiGraph_matplotlib(
            axs[1],
            spsg,
            targetNode=frozenset({B})
        )
        draw_ComputerSetMultiDiGraph_matplotlib(
            axs[0],
            spsg,
            targetNode=frozenset({A})
        )
        fig1.savefig("spsg.pdf")
        plt.close(fig1)
        res = minimal_startnodes_for_node(spsg, targetVars)
        # print('###############################') print('miminal startsets
        # for: ', node_2_string(targetVars),nodes_2_string(res))
        # print('###############################')
        self.assertSetEqual(
            res,
            frozenset({
                frozenset({I, E, F}),
                frozenset({I, C, D}),
                frozenset({I, H, C, G}),
                frozenset({I, H, C, D, G}),
                frozenset({I, E, H, F, G})
            })
        )
