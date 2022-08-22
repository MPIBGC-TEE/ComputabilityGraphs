import networkx as nx
import matplotlib.pyplot as plt
from testinfrastructure.InDirTest import InDirTest
from ComputabilityGraphs.or_graph_helpers import (
    TypeNode,
    TypeLeaf,
    CompTree,
    t_tree,
    c_tree,
    TypeSet,
    AltSet,
    AltSetSet
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


class TestOrGraphs(InDirTest):

    def test_TypeSet(self):
        print(TypeSet([I]))

    def test_AltSet(self):
        print(
            AltSet([
                TypeSet([I])
            ])
        )

    def test_psts(self):
        # leaf
        self.assertEqual( 
            TypeLeaf(I).psts,
            AltSet([TypeSet([I])])
        )

        # comptree with TypeLeafs
        self.assertEqual(
            CompTree(
                root_computer=p_from_i_j_k,
                type_trees = frozenset({
                    TypeLeaf(I),
                    TypeLeaf(J),
                    TypeLeaf(K)
                })
            ).psts,
            AltSet([TypeSet([I,J,K])])
        )

        # comptree with TypeLeafs
        self.assertEqual(
            CompTree(
                root_computer=p_from_r_s,
                type_trees = frozenset({
                    TypeLeaf(R),
                    TypeLeaf(S),
                })
            ).psts,
            AltSet([TypeSet([R, S])])
        )

        # TypeNode with one CompTree
        self.assertEqual(
            TypeNode(
				comp_trees=frozenset([
                    CompTree(
                        root_computer=q_from_i_j_k,
                        type_trees = frozenset([
                            TypeLeaf(I),
                            TypeLeaf(J),
                            TypeLeaf(K)
                        ])
                    )
                ])
            ).psts,
            AltSet([
                TypeSet([I, J, K])
            ])
        )
        # TypeNode with two CompTrees
        self.assertEqual(
            TypeNode(
				comp_trees=frozenset([
                    CompTree(
                        root_computer=p_from_r_s,
                        type_trees = frozenset([
                            TypeLeaf(R),
                            TypeLeaf(S),
                        ])
                    ),
                    CompTree(
                        root_computer=p_from_i_j_k,
                        type_trees = frozenset([
                            TypeLeaf(I),
                            TypeLeaf(J),
                            TypeLeaf(K)
                        ])
                    )
                ])
            ).psts,
            AltSet([
                TypeSet([R, S]),
                TypeSet([I, J, K])
            ])
        )
        # comptree with TypeNodes 
        self.assertEqual(
            CompTree(
                root_computer=g_from_p_q,
                type_trees = frozenset([
                    TypeNode(
        				comp_trees=frozenset([
                            CompTree(
                                root_computer=p_from_r_s,
                                type_trees = frozenset([
                                    TypeLeaf(R),
                                    TypeLeaf(S),
                                ])
                            ),
                            CompTree(
                                root_computer=p_from_i_j_k,
                                type_trees = frozenset([
                                    TypeLeaf(I),
                                    TypeLeaf(J),
                                    TypeLeaf(K)
                                ])
                            )
                        ])
                    ),
                    TypeNode(
				        comp_trees=frozenset([
                            CompTree(
                                root_computer=q_from_i_j_k,
                                type_trees = frozenset([
                                    TypeLeaf(I),
                                    TypeLeaf(J),
                                    TypeLeaf(K)
                                ])
                            )
                        ])
                    )
                ])
            ).psts,
            AltSet([
                TypeSet([R, S, I, J, K]),
                TypeSet([I, J, K])
            ])
        )
    def test_draw_matplotlib(self):
        res = t_tree(
            root_type=G,
            available_computers=ComputerSet([g_from_i_j_k, g_from_p_q]),
            avoid_types=frozenset({}),
        )
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        og = res.to_OrGraph()
        og.draw_matplotlib(ax)
        fig.savefig("OrGraph.pdf")
        # from IPython import embed; embed()
