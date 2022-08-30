# import networkx as nx
import matplotlib.pyplot as plt
from testinfrastructure.InDirTest import InDirTest
# from unittest import TestCase
from ComputabilityGraphs.or_graph_helpers import (
    TypeNode,
    TypeLeaf,
    CompTree,
    t_tree,
    # c_tree,
    TypeSet,
    # AltSet,
    # AltSetSet
)

# from ComputabilityGraphs import helpers as h
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
    k_from_r_s,
    a_from_i,
    b_from_c_d,
    b_from_e_f,
    c_from_b,
    d_from_b,
    d_from_g_h,
    e_from_b,
    f_from_b,
    a_from_b_c, 
    c_from_e_f,
)


class Test_t_tree(InDirTest):

    def test_t_tree_1a(self):
        computers = ComputerSet([
            p_from_r_s,
            p_from_i_j_k
        ])
        res = t_tree(
            root_type=P,
            available_computers=computers,
            avoid_types=frozenset({G})
        )
        print(res)
        ref = TypeNode(
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
        print(ref)
        self.assertEqual(res, ref)    

    def test_t_tree_1b(self):
        computers = ComputerSet([
            q_from_i_j_k
        ])
        res = t_tree(
            root_type=Q,
            available_computers=computers,
            avoid_types=frozenset({G})
        )
        print(res)
        ref = TypeNode(
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

        print(ref)
        self.assertEqual(res, ref)

    def test_t_tree_1c(self):
        computers = ComputerSet([
            j_from_i_p_q
        ])
        res = t_tree(
            root_type=J,
            available_computers=computers,
            avoid_types=frozenset({G})
        ) 
        ref = TypeNode(
            comp_trees=frozenset([
            	CompTree(
            		root_computer=j_from_i_p_q,
            		type_trees = frozenset([
            			TypeLeaf(I),
            			TypeLeaf(P),
            			TypeLeaf(Q),
            		])
                )
            ])
        )         
        self.assertEqual(res, ref)    

    def test_t_tree_1d(self):
        computers = ComputerSet([
            k_from_g_i,
            k_from_r_s
        ])
        res = t_tree(
            root_type=K,
            available_computers=computers,
            avoid_types=TypeSet({G})
        )
        # since g is to be avoided only one possibility to computer k remains
        ref = TypeNode(
	        comp_trees=frozenset([
        	    CompTree(
        	    	root_computer=k_from_r_s,
        	    	type_trees = frozenset([
        	    		TypeLeaf(R),
        	    		TypeLeaf(S),
        	    	])
                )
            ])
        )    
        self.assertEqual(res, ref)    
    
    # top down testing 
    # we limit the recursion level to 1 by the limited computerset
    def test_t_tree_1e(self):
        computers = ComputerSet([g_from_i_j_k, g_from_p_q])
        res = t_tree(
            root_type=G,
            available_computers=computers,
            avoid_types=frozenset({})
        )
        ref = TypeNode(
		    comp_trees=frozenset([
            	CompTree(
            		root_computer=g_from_i_j_k,
            		type_trees = frozenset([
            			TypeLeaf(I),
            			TypeLeaf(J),
            			TypeLeaf(K),
            		])
            	),
            	CompTree(
            		root_computer=g_from_p_q,
            		type_trees = frozenset([
            		    TypeLeaf(P),
            		    TypeLeaf(Q)
                    ])
                )
            ])
        )
        self.assertEqual(res, ref)    

    # second level of recursion   
    def test_t_tree_2a(self):
        computers = ComputerSet([
            g_from_p_q,
            p_from_r_s,
            p_from_i_j_k,
            q_from_i_j_k,
        ])
        res = t_tree(
            root_type=G,
            available_computers=computers,
            avoid_types=frozenset({})
        )
        print(res)
        ref = TypeNode(
            comp_trees=frozenset([
                CompTree(
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
            ])
        )    
        self.assertEqual(res, ref)    

    def test_t_tree_2b(self):
        computers = ComputerSet([
            g_from_i_j_k,
            j_from_i_p_q,
            k_from_g_i,
        ])
        res = t_tree(
            root_type=G,
            available_computers=computers,
            avoid_types=frozenset({})
        )
        print(res)
        ref = TypeNode(
            comp_trees=frozenset([
                CompTree(
                    root_computer=g_from_i_j_k,
                    type_trees=frozenset([
                        TypeLeaf(I),
            	        TypeNode(
                            comp_trees=frozenset([
                                CompTree(
            	        	        root_computer=j_from_i_p_q,
                                	type_trees = frozenset([
                                		TypeLeaf(I),
                                		TypeLeaf(P),
                                		TypeLeaf(Q),
                                	])
                                )
                            ])
                        ),
                        TypeLeaf(K)
                    ])
                )
            ])
        )
        self.assertEqual(res, ref)    

    # 
    def test_t_tree_3(self):
        computers = ComputerSet([
            g_from_p_q,
            p_from_i_j_k,
            q_from_i_j_k,
            g_from_i_j_k,
            j_from_i_p_q,
            k_from_g_i,
        ])
        res = t_tree(
            root_type=G,
            available_computers=computers,
            avoid_types=frozenset({})
        )
        print(res)
        ref=TypeNode(
            comp_trees=frozenset([
                CompTree(
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
                ),
                CompTree(
                    root_computer=g_from_i_j_k,
                    type_trees=frozenset([
                        TypeLeaf(I),
                        TypeNode(   
                            comp_trees=frozenset([
                                CompTree(
                        	         root_computer=j_from_i_p_q,
                                     type_trees = frozenset([
                                		TypeLeaf(I),
                                		TypeLeaf(P),
                                		TypeLeaf(Q),
                                	])
                                )
                            ])
                        ),
                        TypeLeaf(K)
                    ])
                )
            ])
        )
        self.assertEqual(res, ref)    

        og = res.to_networkx_graph(TypeSet({}))
        fig = plt.figure(figsize=(20,20))
        ax = fig.add_subplot(1, 1, 1)
        og.draw_matplotlib(ax)
        fig.savefig("OrGraphNX.pdf")

    def test_t_tree_with_given_variables(self):
        res = t_tree(
            root_type=C,
            available_computers={
                a_from_i,
                a_from_b_c, 
                b_from_c_d,
                c_from_e_f,
                d_from_g_h
            },
            given_types={E, F, G, H}
        )
        ref = TypeNode(
            comp_trees=frozenset([
                CompTree(
                    root_computer=c_from_e_f,
                    type_trees=frozenset([
                        TypeLeaf(E),
                        TypeLeaf(F),
                    ])
                )
            ])
        )
        self.assertTrue(ref == res)
        og_res = res.to_networkx_graph(TypeSet({}))
        og_ref = ref.to_networkx_graph(TypeSet({}))
        fig = plt.figure(figsize=(20,20))
        axs = fig.subplots(2, 1)
        og_res.draw_matplotlib(axs[0])
        og_ref.draw_matplotlib(axs[1])
        fig.savefig("OrGraphNX.pdf")
        

        
