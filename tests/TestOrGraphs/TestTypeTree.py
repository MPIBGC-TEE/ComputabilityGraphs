import matplotlib.pyplot as plt
from testinfrastructure.InDirTest import InDirTest
import matplotlib.gridspec as gridspec

from ComputabilityGraphs.dep_graph_helpers import DepGraph
from ComputabilityGraphs.or_graph_helpers import (
    TypeNode,
    TypeLeaf,
    CompTree,
    # t_tree,
    # c_tree,
    TypeSet,
    # AltSet,
    # AltSetSet
)

from ComputabilityGraphs import helpers as h
from ComputabilityGraphs.ComputerSet import ComputerSet

from ComputabilityGraphs.OrGraphs.MayBeDepGraphs import (
    NoDepGraphs, 
    JustDepGraphs,
    MayBeDepGraphs
)

from testComputers import (
    A,
    B,
    C,
    D,
    E,
    F,
    G,
    H,
    I,
    J,
    K,
    L,
    M,
    N,
    O,
    P,
    Q,
    R,
    S,
    T,
    g_from_i_j_k,
    g_from_p_q,
    h_from_i_l,
    j_from_i_p_q,
    k_from_g_i,
    l_from_h_i,
    o_from_i_k,
    p_from_i_j_k,
    p_from_r_s,
    q_from_i_j_k,
    k_from_r_s,
)


class TestTypeTree(InDirTest):

    def test_computable_depgraphs_0_a(self):
        # computable but empty
        res = TypeLeaf(K).computable_depgraphs(given=TypeSet({K}))
        self.assertTrue(isinstance(res, JustDepGraphs))
        self.assertEqual(len(res.dep_graphs), 1)
        self.assertEqual(list(res.dep_graphs)[0], DepGraph())

    def test_computable_depgraphs_0_b(self):
        # not computable
        res = TypeLeaf(K).computable_depgraphs(given=TypeSet({}))
        self.assertTrue(isinstance(res, NoDepGraphs))

    def test_computable_depgraphs_1(self):
        ct = CompTree(
            root_computer=p_from_i_j_k,
            type_trees=frozenset(
                [
                    TypeLeaf(K),
                    TypeLeaf(J),
                    TypeLeaf(I),
                ]
            ),
        )
        res = ct.computable_depgraphs(given=TypeSet({I, J, K}))
        #from IPython import embed;embed()
        dg = res.dep_graphs[0]

        ref = DepGraph()
        ref.add_node(p_from_i_j_k)

        fig = plt.figure(figsize=(15, 15))
        axs = fig.subplots(2, 1)
        og = ct.to_networkx_graph(avoid_types=TypeSet({}))
        og.draw_matplotlib(axs[0])
        ref.draw_matplotlib(axs[1])
        fig.savefig("OrGraphNX.pdf")
        dg.draw_matplotlib(axs[0])
        self.assertEqual(dg, ref)

    def test_computable_depgraphs_1a(self):
        tt = TypeNode(
            comp_trees=frozenset([
                CompTree(
                    root_computer=p_from_i_j_k,
                    type_trees=frozenset([
                        TypeLeaf(K),
                        TypeLeaf(J),
                        TypeLeaf(I),
                    ])
                )
            ])
        )
        res = tt.computable_depgraphs(frozenset({I,J,K})).result_set
        g = DepGraph()
        g.add_node(p_from_i_j_k)
        ref = frozenset({g})
        
        fig = plt.figure(figsize=(15,15))
        axs = fig.subplots(3, 1)
        og = tt.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(axs[0])
        axs[0].set_title("TypeTree")

        ax=axs[1]
        for e in res:
            e.draw_matplotlib(ax)
        ax.set_title("res")
        
        ax=axs[2]
        for e in ref:
            e.draw_matplotlib(ax)
        ax.set_title("ref")
        fig.savefig("OrGraphNX.pdf")
        self.assertEqual(res,ref)

    def test_computable_depgraphs_1b(self):
        tt = TypeNode(
            comp_trees=frozenset([
                CompTree(
                	root_computer=p_from_i_j_k,
                	type_trees=frozenset([
                		TypeLeaf(K),
                		TypeLeaf(J),
                		TypeLeaf(I),
                	])
                ),
                CompTree(
                	root_computer=p_from_r_s,
                	type_trees=frozenset([
                		TypeLeaf(R),
                		TypeLeaf(S),
                	])
                )
            ])
        )
        ref_1 = DepGraph()
        ref_1.add_node(p_from_i_j_k)
        
        ref_2 = DepGraph()
        ref_2.add_node(p_from_r_s)

        
        res = tt.computable_depgraphs({I,J,K,R,S})
        
        fig = plt.figure(figsize=(15, 15))
        axs = fig.subplots(3, 1)
        og = tt.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(axs[0])
        ref_1.draw_matplotlib(axs[1])
        ref_2.draw_matplotlib(axs[2])
        fig.savefig("OrGraphNX.pdf")
        print(res.result_set)
        self.assertEqual(res.result_set, frozenset({ref_1,ref_2}))

    def test_computable_depgraphs_2_a(self):
        ct = CompTree(
            root_computer=g_from_p_q,
            type_trees=frozenset([
                TypeNode(
                    comp_trees=frozenset([
                        CompTree(
                            root_computer=p_from_i_j_k,
                            type_trees=frozenset([
                                TypeLeaf(K),
                                TypeLeaf(J),
                                TypeLeaf(I),
                            ])
                        ),
                        CompTree(
                            root_computer=p_from_r_s,
                            type_trees=frozenset([
                                TypeLeaf(R),
                                TypeLeaf(S),
                            ])
                            )
                        ])
                ),
                TypeNode(
                   comp_trees=frozenset([
                       CompTree(
                           root_computer=q_from_i_j_k,
                           type_trees=frozenset([
                              TypeLeaf(K),
                              TypeLeaf(J),
                              TypeLeaf(I),
                           ])
                       )
                   ])
                )
            ])
        )
        # This time one of the paths is impossible since S is missing
        given=frozenset({I, J, K ,R})
        res=ct.computable_depgraphs(given)
        ref_1 = DepGraph()
        ref_1.add_edges_from([
            (g_from_p_q, p_from_i_j_k),
            (g_from_p_q, q_from_i_j_k),
        ])
        
        #ref_2 = DepGraph()
        #ref_2.add_edges_from([
        #    (g_from_p_q, p_from_r_s),
        #    (g_from_p_q, q_from_i_j_k),
        #])

        fig = plt.figure(figsize=(15, 15))
        gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[2, 1, 1])
        og = ct.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(fig.add_subplot(gs[0,:]))
        ref_1.draw_matplotlib(fig.add_subplot(gs[1,0]))
        #ref_2.draw_matplotlib(fig.add_subplot(gs[1,1]))
        
        rrs = res.result_set
        for i,dg in enumerate(rrs):
            dg.draw_matplotlib(fig.add_subplot(gs[2,i]))
        fig.savefig("OrGraphNX.pdf")

        self.assertEqual(rrs, frozenset({ref_1}))
        #ref_1.draw_matplotlib(axs[1])
    
    def test_computable_depgraphs_2_b(self):
        ct = CompTree(
            root_computer=g_from_p_q,
            type_trees=frozenset([
                TypeNode(
                    comp_trees=frozenset([
                        CompTree(
                            root_computer=p_from_i_j_k,
                            type_trees=frozenset([
                                TypeLeaf(K),
                                TypeLeaf(J),
                                TypeLeaf(I),
                            ])
                        ),
                        CompTree(
                            root_computer=p_from_r_s,
                            type_trees=frozenset([
                                TypeLeaf(R),
                                TypeLeaf(S),
                            ])
                            )
                        ])
                ),
                TypeNode(
                   comp_trees=frozenset([
                       CompTree(
                           root_computer=q_from_i_j_k,
                           type_trees=frozenset([
                              TypeLeaf(K),
                              TypeLeaf(J),
                              TypeLeaf(I),
                           ])
                       )
                   ])
                )
            ])
        )
        given=frozenset({I, J, K, R, S})
        res=ct.computable_depgraphs(given)
        ref_1 = DepGraph()
        ref_1.add_edges_from([
            (g_from_p_q, p_from_i_j_k),
            (g_from_p_q, q_from_i_j_k),
        ])
        
        ref_2 = DepGraph()
        ref_2.add_edges_from([
            (g_from_p_q, p_from_r_s),
            (g_from_p_q, q_from_i_j_k),
        ])

        fig = plt.figure(figsize=(15, 15))
        gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[2, 1, 1])
        og = ct.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(fig.add_subplot(gs[0,:]))
        ref_1.draw_matplotlib(fig.add_subplot(gs[1,0]))
        ref_2.draw_matplotlib(fig.add_subplot(gs[1,1]))
        
        rrs = res.result_set
        for i,dg in enumerate(rrs):
            dg.draw_matplotlib(fig.add_subplot(gs[2,i]))
        fig.savefig("OrGraphNX.pdf")

        self.assertEqual(rrs, frozenset({ref_1,ref_2}))
        #ref_1.draw_matplotlib(axs[1])
