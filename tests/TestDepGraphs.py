import networkx as nx
import matplotlib.pyplot as plt
from testinfrastructure.InDirTest import InDirTest
from ComputabilityGraphs import dep_graph_helpers as dgh
from ComputabilityGraphs import helpers as h
from ComputabilityGraphs.ComputerSet import ComputerSet

from testComputers import (
    A, B, C, D, E, F, G, H, I, 
    a_from_i,
    a_from_b_c,
    b_from_c_d,
    c_from_e_f,
    d_from_g_h,
)

class TestDepGraphs(InDirTest):

    def test_draw_matplotlib(self):
        g=dgh.DepGraph()
        g.add_edge(b_from_c_d,c_from_e_f)
        g.add_edge(b_from_c_d,d_from_g_h)
        fig=plt.figure();
        ax=fig.subplots(1,1)
        g.draw_matplotlib(ax)
        fig.savefig("dep_graph.pdf")
    
    def test_dep_graph(self):
        cs=ComputerSet({
            a_from_i,
            b_from_c_d,
            c_from_e_f,
            d_from_g_h,
        })
        given={E, F, G, H}

        g_ref = dgh.DepGraph()
        g_ref.add_node(c_from_e_f)
        
        g_res = dgh.dep_graph(
            root_type=C,
            cs=cs,
            given=given
        )

        fig=plt.figure();
        ax1,ax2 = fig.subplots(2,1)
        g_ref.draw_matplotlib(ax1)
        g_res.draw_matplotlib(ax2)
        fig.savefig("dep_graph_c(e,f).pdf")
        self.assertEqual(g_res,g_ref)
        
        g_ref = dgh.DepGraph()
        g_ref.add_node(d_from_g_h)
        
        g_res = dgh.dep_graph(
            root_type=D,
            cs=cs,
            given=given
        )

        fig=plt.figure();
        ax1,ax2 = fig.subplots(2,1)
        g_ref.draw_matplotlib(ax1)
        g_res.draw_matplotlib(ax2)
        fig.savefig("dep_graph_d(g,h).pdf")
        self.assertEqual(g_res,g_ref)


        g_ref = dgh.DepGraph()
        g_ref.add_edge(b_from_c_d,c_from_e_f)
        g_ref.add_edge(b_from_c_d,d_from_g_h)
        
        g_res = dgh.dep_graph(
            root_type=B,
            cs=cs,
            given=given
        )

        fig=plt.figure();
        ax1,ax2 = fig.subplots(2,1)
        g_ref.draw_matplotlib(ax1)
        g_res.draw_matplotlib(ax2)
        fig.savefig("dep_graph_b(c,d).pdf")
        self.assertEqual(g_res,g_ref)

    def test_dep_graph_2(self):
        cs=ComputerSet({
            a_from_b_c,
            b_from_c_d,
            c_from_e_f,
            d_from_g_h,
        })
        given={E, F, G, H}
        g_res = dgh.dep_graph(
            root_type=A,
            cs=cs,
            given=given
        )
    
        g_ref = dgh.DepGraph()
        g_ref.add_edge(a_from_b_c,b_from_c_d)
        g_ref.add_edge(a_from_b_c,c_from_e_f)

        g_ref.add_edge(b_from_c_d,c_from_e_f)
        g_ref.add_edge(b_from_c_d,d_from_g_h)

        fig=plt.figure();
        ax1,ax2 = fig.subplots(2,1)
        g_ref.draw_matplotlib(ax1)
        g_res.draw_matplotlib(ax2)
        fig.savefig("dep_graph_a(b,c).pdf")
        self.assertEqual(g_res,g_ref)
        self.assertEqual(g_res.edges, g_ref.edges)
    

    def test_required_mvars(self):
        g = dgh.DepGraph()
        g.add_edge(b_from_c_d,c_from_e_f)
        g.add_edge(b_from_c_d,d_from_g_h)

        ref = frozenset([E,F,G,H])
        self.assertEqual(ref,g.required_mvars())


    def test_all_computer_combies(self):
        given=frozenset({E, F, G, H})
        cs = frozenset({
            a_from_i,
            a_from_b_c, 
            b_from_c_d,
            c_from_e_f,
            d_from_g_h
        })
        res = dgh.computer_combies(
            cs,
            given=frozenset({E, F, G, H})
        )
        print(res)


    def test_all_dep_graphs(self):
        cs=frozenset({
            a_from_i,
            a_from_b_c, 
            b_from_c_d,
            c_from_e_f,
            d_from_g_h
        })
        provided_values = {
            E(1),
            F(1),
            G(1),
            H(1)
        }
        given={E, F, G, H}
        g_ref_1 = nx.DiGraph()
        g_ref_1.add_edge(b_from_c_d,c_from_e_f)
        g_ref_1.add_edge(b_from_c_d,d_from_g_h)

        gs= list(
            dgh.all_dep_graphs(
                root_type=A,
                cs=cs,
                given=given
            )
        )
        fig=plt.figure()
        axs = fig.subplots(len(gs),1)
        print(len(axs))
        for i,ax in enumerate(axs):
            g = gs[i]
            print(g)
            print(g.required_mvars())
            g.draw_matplotlib(ax)
        fig.savefig("graphs.pdf")


    def test_computable_dep_graphs_1(self):
        given=frozenset({E, F, G, H})
        cs = frozenset({
            a_from_i,
            a_from_b_c, 
            b_from_c_d,
            c_from_e_f,
            d_from_g_h
        })
        gs= list(
            dgh.computable_dep_graphs(
                root_type=A,
                cs=cs,
                given=given
            )
        )
        fig=plt.figure()
        ax  = fig.subplots(1)
        g = gs[0]
        print(g)
        print(g.required_mvars())
        g.draw_matplotlib(ax)
        fig.savefig("graphs.pdf")
        
        g_ref = dgh.DepGraph()
        g_ref.add_edge(a_from_b_c,b_from_c_d)
        g_ref.add_edge(a_from_b_c,c_from_e_f)

        g_ref.add_edge(b_from_c_d,c_from_e_f)
        g_ref.add_edge(b_from_c_d,d_from_g_h)
        self.assertEqual(g_ref,g)


    def test_computable_dep_graphs_2(self):
        # this time there are two ways to compute A
        given=frozenset({E, F, G, H, I})
        cs = frozenset({
            a_from_i,
            a_from_b_c, 
            b_from_c_d,
            c_from_e_f,
            d_from_g_h
        })
        gs= list(
            dgh.computable_dep_graphs(
                root_type=A,
                cs=cs,
                given=given
            )
        )

        fig=plt.figure()
        axs = fig.subplots(len(gs),1)
        for i,ax in enumerate(axs):
            gs[i].draw_matplotlib(ax)
        fig.savefig("graphs.pdf")
        
        g_ref_1 = dgh.DepGraph()
        g_ref_1.add_node(a_from_i)

        g_ref_2 = dgh.DepGraph()
        g_ref_2.add_edge(a_from_b_c,b_from_c_d)
        g_ref_2.add_edge(a_from_b_c,c_from_e_f)

        g_ref_2.add_edge(b_from_c_d,c_from_e_f)
        g_ref_2.add_edge(b_from_c_d,d_from_g_h)
        self.assertEqual(
            set(gs),
            set([g_ref_1,g_ref_2])
        )


    def test_shortest_computable_dep_graph(self):
        # this time there are two ways to compute A
        given=frozenset({E, F, G, H, I})
        cs = frozenset({
            a_from_i,
            a_from_b_c, 
            b_from_c_d,
            c_from_e_f,
            d_from_g_h
        })
        res = dgh.shortest_computable_dep_graph(
            root_type=A,
            cs=cs,
            given=given
        )

        fig=plt.figure()
        ax  = fig.subplots(1)
        res.draw_matplotlib(ax)
        fig.savefig("graphs.pdf")

        g_ref_1 = dgh.DepGraph()
        g_ref_1.add_node(a_from_i)

        self.assertEqual( res, g_ref_1)



