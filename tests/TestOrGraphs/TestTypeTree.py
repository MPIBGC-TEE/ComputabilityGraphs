import matplotlib.pyplot as plt
from testinfrastructure.InDirTest import InDirTest
from ComputabilityGraphs.dep_graph_helpers import (DepGraph)
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
    k_from_r_s

)


class TestTypeTree(InDirTest):
    def test_depgraphs_0(self):
        ct = CompTree(
        	root_computer=p_from_i_j_k,
        	type_trees=frozenset([
        		TypeLeaf(K),
        		TypeLeaf(J),
        		TypeLeaf(I),
        	])
        )
        res = ct.depgraph().dg
        

        ref = DepGraph()
        ref.add_node(p_from_i_j_k)
        
        fig = plt.figure(figsize=(15,15))
        axs = fig.subplots(2, 1)
        og = ct.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(axs[0])
        ref.draw_matplotlib(axs[1])
        fig.savefig("OrGraphNX.pdf")
        res.draw_matplotlib(axs[0])
        self.assertEqual(res, ref)

    def test_depgraphs_1a(self):
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
        res = tt.depgraph()
        ref = DepGraph()
        ref.add_node(p_from_i_j_k)


        fig = plt.figure(figsize=(15,15))
        axs = fig.subplots(2, 1)
        og = tt.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(axs[0])
        ref.draw_matplotlib(axs[1])
        fig.savefig("OrGraphNX.pdf")


    def test_depgraphs_1b(self):
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

        res = tt.depgraph()

        fig = plt.figure(figsize=(15, 15))
        axs = fig.subplots(3, 1)
        og = tt.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(axs[0])
        ref_1.draw_matplotlib(axs[1])
        ref_2.draw_matplotlib(axs[2])
        fig.savefig("OrGraphNX.pdf")
        self.assertTrue((res.dg == ref_1) or (res.dg == ref_2))

    def test_depgraphs_2(self):
        ct = CompTree(
            root_computer=g_from_p_q,
            type_trees=frozenset([
                TypeNode(
                    comp_trees=frozenset([
                        #CompTree(
                        #    root_computer=p_from_i_j_k,
                        #    type_trees=frozenset([
                        #        TypeLeaf(K),
                        #        TypeLeaf(J),
                        #        TypeLeaf(I),
                        #    ])
                        #),
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
        res=ct.depgraph().dg
        fig = plt.figure(figsize=(15, 15))
        axs = fig.subplots(3, 1)
        og = ct.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(axs[0])
        ref = DepGraph()
        ref.add_edge(g_from_p_q, p_from_r_s)
        ref.add_edge(g_from_p_q, q_from_i_j_k)
        res.draw_matplotlib(axs[1])
        ref.draw_matplotlib(axs[2])
        fig.savefig("OrGraphNX.pdf")
        self.assertEqual(ref,res)
