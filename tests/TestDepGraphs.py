import networkx as nx
import matplotlib.pyplot as plt
from testinfrastructure.InDirTest import InDirTest
from ComputabilityGraphs import dep_graph_helpers as dgh
from ComputabilityGraphs.ComputerSet import ComputerSet

from testComputers import (
    B, C, D, E, F, G, H, 
    a_from_i,
    b_from_c_d,
    c_from_e_f,
    d_from_g_h,
)

class TestDepGraphs(InDirTest):

    def test_draw_matplotlib(self):
        g=nx.DiGraph()
        g.add_edge(b_from_c_d,c_from_e_f)
        g.add_edge(b_from_c_d,d_from_g_h)
        fig=plt.figure();
        ax=fig.subplots(1,1)
        dgh.draw_matplotlib(g,ax)
        fig.savefig("dep_graph.pdf")
    
    def test_dep_graph(self):
        cs=ComputerSet({
            a_from_i,
            b_from_c_d,
            c_from_e_f,
            d_from_g_h,
        })
        given={E, F, G, H}

        g_ref = nx.DiGraph()
        g_ref.add_node(c_from_e_f)
        
        g_res = dgh.dep_graph(
            root_type=C,
            cs=cs,
            given=given
        )
        #from IPython import embed;embed()
        fig=plt.figure();
        ax1,ax2 = fig.subplots(2,1)
        dgh.draw_matplotlib(g_ref,ax1)
        dgh.draw_matplotlib(g_res,ax2)
        fig.savefig("dep_graph_c(e,f).pdf")
        self.assertEqual(g_res.edges(),g_ref.edges())
        
        g_ref = nx.DiGraph()
        g_ref.add_node(d_from_g_h)
        
        g_res = dgh.dep_graph(
            root_type=D,
            cs=cs,
            given=given
        )
        #from IPython import embed;embed()
        fig=plt.figure();
        ax1,ax2 = fig.subplots(2,1)
        dgh.draw_matplotlib(g_ref,ax1)
        dgh.draw_matplotlib(g_res,ax2)
        fig.savefig("dep_graph_d(g,h).pdf")
        self.assertEqual(g_res.edges(),g_ref.edges())


        g_ref = nx.DiGraph()
        g_ref.add_edge(b_from_c_d,c_from_e_f)
        g_ref.add_edge(b_from_c_d,d_from_g_h)
        
        g_res = dgh.dep_graph(
            root_type=B,
            cs=cs,
            given=given
        )
        #from IPython import embed;embed()
        fig=plt.figure();
        ax1,ax2 = fig.subplots(2,1)
        dgh.draw_matplotlib(g_ref,ax1)
        dgh.draw_matplotlib(g_res,ax2)
        fig.savefig("dep_graph_b(c,d).pdf")
        self.assertEqual(g_res.edges(),g_ref.edges())
        
