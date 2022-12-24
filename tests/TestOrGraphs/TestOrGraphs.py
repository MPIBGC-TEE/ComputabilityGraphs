import networkx as nx
import matplotlib.pyplot as plt
import igraph as ig
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
                type_trees=frozenset([
                    TypeNode(
                        comp_trees=frozenset([
                            CompTree(
                                root_computer=p_from_r_s,
                                type_trees=frozenset([
                                    TypeLeaf(R),
                                    TypeLeaf(S),
                                ])
                            ),
                            CompTree(
                                root_computer=p_from_i_j_k,
                                type_trees=frozenset([
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
                                type_trees=frozenset([
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
        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(1, 1, 1)
        og = res.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(ax)
        fig.savefig("OrGraphNX.pdf")

    def test_draw_matplotlib_with_given(self):
        res = t_tree(
            root_type=G,
            available_computers=ComputerSet([g_from_i_j_k, g_from_p_q]),
            avoid_types=frozenset({}),
        )
        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(1, 1, 1)
        og = res.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(ax,given={I,K,Q})
        fig.savefig("OrGraphNX.pdf")
        # from IPython import embed; embed()

    def test_draw_matplotlib_with_type_aliases(self):
        computers = ComputerSet([g_from_i_j_k, g_from_p_q])
        res = t_tree(
            root_type=G,
            available_computers=computers,
            avoid_types=frozenset({}),
        )
        import string
        from ComputabilityGraphs import helpers as cgh
        t_abbreviations = [f"{ul}" for ul in string.ascii_uppercase]
        c_abbreviations = [f"{ll}" for ll in string.ascii_lowercase]
        type_aliases = {
            t:t_abbreviations[i] 
            for i,t in enumerate(cgh.all_mvars(computers))
        }
        computer_aliases = {
            c:c_abbreviations[i] 
            for i,c in enumerate(computers)
        }
        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(1, 1, 1)
        og = res.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        og.draw_matplotlib(
            ax,
            type_aliases=type_aliases,
            computer_aliases=computer_aliases
        )
        fig.savefig("OrGraphNX.pdf")
        # from IPython import embed; embed()
    
    def test_jupyter_widget(self):
        computers = ComputerSet([g_from_i_j_k, g_from_p_q])
        res = t_tree(
            root_type=G,
            available_computers=computers,
            avoid_types=frozenset({}),
        )
        import string
        from ComputabilityGraphs import helpers as cgh
        t_abbreviations = [f"{ul}" for ul in string.ascii_uppercase]
        c_abbreviations = [f"{ll}" for ll in string.ascii_lowercase]
        type_aliases = {
            t:t_abbreviations[i] 
            for i,t in enumerate(cgh.all_mvars(computers))
        }
        computer_aliases = {
            c:c_abbreviations[i] 
            for i,c in enumerate(computers)
        }
        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(1, 1, 1)
        key_func= lambda s: ord(s)
        res.jupyter_widget(
            (type_aliases, key_func),
            (computer_aliases, key_func)
        )

    def test_draw_igraph(self):
        # incomplete, but the layout works very well 
        res = t_tree(
            root_type=G,
            available_computers=ComputerSet([g_from_i_j_k, g_from_p_q]),
            avoid_types=frozenset({}),
        )
        og = res.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        IG= ig.Graph.from_networkx(og) 
        vertex_size = [10 for v in IG.vs]
        labels = [v for v in IG.vs]

        #edge_color_dict = {'in':'blue','internal':'black','out':'red'}
        #edge_colors = [edge_color_dict[e['type']] for e in IG.es]
        layout=IG.layout('sugiyama')
         
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ig.plot(
            IG,
            layout=layout,
            vertex_size=vertex_size,
            vertex_label=labels,
            #edge_color=edge_colors
            target=ax
        )
        fig.savefig("IGraph.pdf")

    def test_draw_igraph_with_given(self):
        # incomplete, but the layout works very well 
        res = t_tree(
            root_type=G,
            available_computers=ComputerSet([g_from_i_j_k, g_from_p_q]),
            avoid_types=frozenset({}),
        )
        og = res.to_networkx_graph(
            avoid_types=TypeSet({})
        )
        IG= ig.Graph.from_networkx(og) 
        vertex_size = [10 for v in IG.vs]
        labels = [v for v in IG.vs]

        #edge_color_dict = {'in':'blue','internal':'black','out':'red'}
        #edge_colors = [edge_color_dict[e['type']] for e in IG.es]
        layout=IG.layout('sugiyama')
         
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ig.plot(
            IG,
            layout=layout,
            vertex_size=vertex_size,
            vertex_label=labels,
            #edge_color=edge_colors
            target=ax
        )
        fig.savefig("IGraph.pdf")
