#import testComputers as tC
from copy import deepcopy
from ComputabilityGraphs.ComputerSetSet import ComputerSetSet
from ComputabilityGraphs.ComputerSet import ComputerSet
import matplotlib.pyplot as plt
from unittest import skip
from testinfrastructure.InDirTest import InDirTest
from ComputabilityGraphs.rec_graph_helpers import  rec_graph_maker
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
from ComputabilityGraphs.Decomposition import Decomposition
from ComputabilityGraphs.Node import Node
from ComputabilityGraphs.ComputerSet import ComputerSet
from ComputabilityGraphs.FastGraph import FastGraph

import ComputabilityGraphs.fast_graph_helpers as fgh
class TestRecGraph(InDirTest):
    def test_node_graph_1(self):
        # the startnode contains avoid_nodes 
        # (halting immidiately)
        # returning original (empty) graph
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
                c_from_b,
                d_from_g_h,
            ]
        )

        _, node_graph = rec_graph_maker(computers) 

        g = FastGraph()
        sn = Node([B,D])
        
        self.assertEqual(
            node_graph(
                g,
                prospective_start_nodes=frozenset([sn]),
                avoid_nodes=frozenset(
                    [
                        Node([B]),
                        Node([C,D])
                    ]
                )
            ),
            FastGraph()
            #(FastGraph(),frozenset())
        )

    def test_decomp_graph_1(self):
        # The active Node of the Decomposition is {B}
        # which is a superset of one of the avoid nodes {{B}.{C,D}}
        # So The returned Graph is empty
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
                c_from_b,
                d_from_g_h,
            ]
        )

        decomp_graph, _ = rec_graph_maker(computers) 
        g = FastGraph()
        sn = Decomposition(
                active=Node([B]),
                passive=Node([D])
        )
        
        self.assertEqual(
            decomp_graph(
                decomposition=sn,
                avoid_nodes=frozenset(
                    [
                        Node([B]),
                        Node([C,D])
                    ]
                )
            ),
            FastGraph()
        )


    def test_decomp_graph_2(self):
        # The active Node of the Decomposition is {B} There is one computer to
        # compute B so the returned Graph will just be ({B}{})<-{C,D}
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
            ]
        )

        decomp_graph, _ = rec_graph_maker(computers) 
        g = FastGraph()
        d = Decomposition(
                active=Node([B]),
                passive=Node()
        )
        cs=ComputerSet([b_from_c_d])
       
        g_ref = FastGraph()
        g_ref.add_unconnected_Decomp(d)
        g_ref.add_connected_Node(
            node=Node([C,D]),
            target_decomp=d,
            computer_sets=frozenset([cs])
        )
        g_res = decomp_graph(
            decomposition=d,
            avoid_nodes=frozenset()
        )
        fig=plt.figure(figsize=(10,20))
        axs=fig.subplots(2,1)
        g_res.draw_matplotlib(axs[0])
        g_ref.draw_matplotlib(axs[1])
        fig.savefig('figure.pdf')


        self.assertEqual(
            g_res,
            g_ref
        )

    def test_node_graph_2(self):
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
            ]
        )

        _, node_graph = rec_graph_maker(computers) 

        g = FastGraph()
        sn = Node([B])
        
        d = Decomposition(
                active=Node([B]),
                passive=Node()
        )
        cs=ComputerSet([b_from_c_d])
        
        g_ref = FastGraph()
        g_ref.add_Node(sn)
        g_ref.add_Decomp(targetNode=sn,decomp=d)
        g_ref.add_connected_Node(
            node=Node([C,D]),
            target_decomp=d,
            computer_sets=frozenset([cs])
        )
        
        g_res = node_graph(
            FastGraph(),
            prospective_start_nodes=frozenset([sn]),
            avoid_nodes=frozenset()
        )

        fig=plt.figure(figsize=(10,20))
        axs=fig.subplots(2,1)
        g_res.draw_matplotlib(axs[0])
        g_ref.draw_matplotlib(axs[1])
        fig.savefig('figure.pdf')
        print(g_res.dg.edges)

        self.assertEqual(
            g_res,
            g_ref
        )
   


    def test_decomp_graph_3(self):
        # test the case where there is one node
        # in the graph that has a child graph attached
        # to it which is generated by iterating over 
        # the decompostions
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
                c_from_b,
                d_from_g_h,
            ]
        )
    
        decomp_graph, _ = rec_graph_maker(computers) 
       
        g = FastGraph()
        d=Decomposition(
            active=Node({C}),
            passive=Node({G,H})
        )
        #n=Node([C])
        #g.add_Node(n)
    
        res= decomp_graph(
            decomposition=d,
            avoid_nodes=frozenset(
                [
                    #Node([B]),
                    Node([C,D]),
                    Node([C,G,H])
                ]
            )
        )

    
        ref = FastGraph()
        ref.add_unconnected_Decomp(d)
        ref.add_connected_Node(
            node=Node([B,G,H]),
            target_decomp=d,
            computer_sets=ComputerSetSet({
                ComputerSet({c_from_b})
            })
        )
        
        fig=plt.figure(figsize=(10,20))
        axs=fig.subplots(2,1)
        res.draw_matplotlib(axs[0])
        ref.draw_matplotlib(axs[1])
        fig.savefig('figure.pdf')
        
        self.assertEqual(
            res,
            ref
        )


    def test_node_graph_3(self):
        # test the case where there is one node
        # in the graph that has a child graph attached
        # to it which is generated by iterating over 
        # the decompostions
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
                c_from_b,
                d_from_g_h,
            ]
        )
    
        _, node_graph = rec_graph_maker(computers) 
       
        g = FastGraph()
        n = Node({C,G,H})
        d = Decomposition(
            active=Node({C}),
            passive=Node({G,H})
        )
    
        res= node_graph(
            FastGraph(),
            prospective_start_nodes=frozenset([n]),
            avoid_nodes=frozenset(
                [
                    Node([C,D]),
                ]
            )
        )

    
        ref = FastGraph()
        ref.add_Node(n)
        ref.add_Decomp(
            decomp=d,
            targetNode=n
        )
        ref.add_connected_Node(
            node=Node([B,G,H]),
            target_decomp=d,
            computer_sets=ComputerSetSet({
                ComputerSet({c_from_b})
            })
        )
        
        fig=plt.figure(figsize=(10,20))
        axs=fig.subplots(2,1)
        res.draw_matplotlib(axs[0])
        ref.draw_matplotlib(axs[1])
        fig.savefig('figure.pdf')
        
        self.assertEqual(
            res,
            ref
        )
    

    def test_node_graph_3b(self):
        # test the case where there is one node
        # in the graph that has a child graph attached
        # to it which is generated by iterating over 
        # the decompostions
        computers = frozenset(
            [
                a_from_i,
                b_from_c_d,
                c_from_b,
                d_from_g_h,
            ]
        )
    
        _, node_graph = rec_graph_maker(computers) 
       
        n0  = Node({B})
        d0a = Decomposition(
            active=n0,
            passive=Node()
        )
        n0a0 = Node({C,D})
        d0a0a = Decomposition(
                active=Node({D}),
                passive=Node({C})
        )
        n0a0a0 = Node({G,H,C})

    
        res= node_graph(
            FastGraph(),
            prospective_start_nodes=frozenset([n0]),
            avoid_nodes=frozenset()
        )

    
        ref = FastGraph()
        ref.add_Node(n0)
        ref.add_Decomp(
            decomp=d0a,
            targetNode=n0
        )
        ref.add_connected_Node(
            node=n0a0,
            target_decomp=d0a,
            computer_sets=ComputerSetSet([
                ComputerSet([
                    b_from_c_d
                ])
            ])
        )
        ref.add_Decomp(
            decomp=d0a0a,
            targetNode=n0a0
        )
        ref.add_connected_Node(
            node=n0a0a0,
            target_decomp=d0a0a,
            computer_sets=ComputerSetSet({
                ComputerSet({d_from_g_h})
            })
        )
        
        fig=plt.figure(figsize=(10,20))
        axs=fig.subplots(2,1)
        res.draw_matplotlib(axs[0])
        ref.draw_matplotlib(axs[1])
        fig.savefig('figure.pdf')
        
        self.assertEqual(
            res,
            ref
        )
   # 
   # def test_rec_graph_2b(self):
   #     # test the case where there is one node
   #     # in the graph that has a child graph attached
   #     # to it which is generated by iterating over 
   #     # the decompostions
   #     computers = frozenset(
   #         [
   #             a_from_i,
   #             b_from_c_d,
   #             c_from_b,
   #             d_from_g_h,
   #         ]
   #     )

   #     rec_graph = rec_graph_maker(computers) 
   #    
   #     g = FastGraph()
   #     n=Node([G,H,C])

   #     res = rec_graph(
   #         g,
   #         prospective_start_nodes=frozenset([n]),
   #         avoid_nodes=frozenset(
   #             [
   #                 #Node([B]),
   #                 Node([C,D]),
   #             ]
   #         )
   #     )

   #    
   #     ref = FastGraph()
   #     ref.add_Node(n)

   #     fig=plt.figure(figsize=(10,20))
   #     axs=fig.subplots(2,1)
   #     res.draw_matplotlib(axs[0])
   #     ref.draw_matplotlib(axs[1])
   #     fig.savefig('figure.pdf')

   #     self.assertEqual(
   #         res,
   #         ref
   #     )

   # def test_rec_graph_3(self):
   #     # empty subgraph (halting because of nodes)
   #     computers = frozenset(
   #         [
   #             a_from_i,
   #             b_from_c_d,
   #             #b_from_e_f,
   #             c_from_b,
   #             #d_from_b,
   #             d_from_g_h,
   #             #e_from_b,
   #             #f_from_b,
   #         ]
   #     )

   #     rec_graph = rec_graph_maker(computers) 
   #    
   #     res = rec_graph(
   #         g=FastGraph(),
   #         start_node=Node([G,H,C]),
   #         avoid_nodes=frozenset(
   #             [
   #                 Node([B]),
   #                 Node([C,D])
   #             ]
   #         )
   #     )

   #    
   #     ref = FastGraph()
   #     ref.add_Node(Node([G,H,C]))

   #     fig=plt.figure()
   #     axs=fig.subplots(2,1)
   #     res.draw_matplotlib(axs[0])
   #     ref.draw_matplotlib(axs[1])
   #     fig.savefig('update.pdf')

   #     self.assertEqual(
   #         res,
   #         ref
   #     )

    def test_add_passive(self):
        # when we add a new subgraph
        # we compute it first from the active node of 
        # a decomposition and then add the passive part
        # to all its nodes and (passive part of the decompositions)
        g = FastGraph()
        g.add_Node(Node([C]))
        g_res = fgh.add_passive(g,Node([G,H]))
        
        g_ref = FastGraph()
        g_ref.add_Node(Node([G,C,H]))
        
        fig=plt.figure(figsize=(10,20))
        axs=fig.subplots(2,1)
        g_res.draw_matplotlib(axs[0])
        g_ref.draw_matplotlib(axs[1])
        fig.savefig('figure1.pdf')
        self.assertEqual(
            g_res,
            g_ref
        )
       
        g = FastGraph()
        n=Node([C])
        g.add_Node(n)
        d=Decomposition(active=Node([C]),passive=Node())
        g.add_Decomp(targetNode=n,decomp=d)
        n1=Node([B])
        g.add_connected_Node(
            node=n1,
            target_decomp=d,
            computer_sets=frozenset([ComputerSet([c_from_b])])
        )

        g_res = fgh.add_passive(g,Node([G,H]))
        
        g_ref = FastGraph()
        na=Node([C,G,H])
        g_ref.add_Node(na)
        da=Decomposition(active=Node([C]),passive=Node([G,H]))
        g_ref.add_Decomp(targetNode=na,decomp=da)
        n1a=Node([B,G,H])
        g_ref.add_connected_Node(
            node=n1a,
            target_decomp=da,
            computer_sets=frozenset([ComputerSet([c_from_b])])
        )
        fig=plt.figure(figsize=(10,20))
        axs=fig.subplots(2,1)
        g_res.draw_matplotlib(axs[0])
        g_ref.draw_matplotlib(axs[1])
        fig.savefig('figure2.pdf')
        self.assertEqual(
            g_res,
            g_ref
        )
            
    def test_connect(self):
        g = FastGraph()
        n = Node([C,D])
        d0 = Decomposition(active=Node([D]),passive=Node([C]))
        g.add_Node(n)
        g.add_Decomp(decomp=d0,targetNode=n)
        
        g_ref = deepcopy(g)
        
        t00 = Node([G,H,C])
        computer_sets=frozenset(
            [ComputerSet([d_from_g_h])
        ])
        g.connect_Node_2_Decomposition(
            node=t00,
            target_decomp=d0,
            computer_sets=computer_sets
        )

        g_ref.add_connected_Node(
            t00,
            target_decomp=d0,
            computer_sets=computer_sets
        )
        self.assertEqual(
            g,
            g_ref
        )


    def test_combine_1(self):
        g1 = FastGraph()
        n = Node([C,D])
        d0 = Decomposition(active=Node([D]),passive=Node([C]))
        g1.add_Node(n)
        g1.add_Decomp(decomp=d0,targetNode=n)
        
        
        g2 = FastGraph()
        g2.add_unconnected_Decomp(decomp=d0)
        t00 = Node([G,H,C])
        computer_sets=frozenset(
            [ComputerSet([d_from_g_h])
        ])
        g2.add_connected_Node(node=t00,target_decomp=d0,computer_sets=computer_sets)
        
        g_res = fgh.combine(g1, g2)

        g_ref = deepcopy(g1)
        g_ref.add_connected_Node(
            t00,
            target_decomp=d0,
            computer_sets=computer_sets
        )
        fig=plt.figure()
        axs=fig.subplots(4,1)
        g1.draw_matplotlib(axs[0])
        g2.draw_matplotlib(axs[1])
        g_res.draw_matplotlib(axs[2])
        g_ref.draw_matplotlib(axs[3])
        fig.savefig('figure.pdf')
        self.assertEqual(
            g_res,
            g_ref
        )

    def test_combine_2(self):
        g1 = FastGraph()
        n1 = Node([C,D])
        d1 = Decomposition(active=Node([B]),passive=Node())
        css=ComputerSetSet([
            ComputerSet([b_from_c_d])
        ])
        g1.add_Node(n1)
        g1.add_unconnected_Decomp( decomp=d1)
        g1.add_connected_Node(
            node=n1,
            target_decomp=d1,
            computer_sets=css
        )

        g2 = FastGraph()
        n2 = Node([B])
        d2 = Decomposition(active=Node([B]),passive=Node())
        g2.add_Node(n2)
        g2.add_Decomp(decomp=d2,targetNode=n2)
        
        g_ref = deepcopy(g1)
        g_ref.add_Node(n2)
        g_ref.connect_Decomposition_2_Node(decomp=d2,target_node=n2)
        
        g_res = fgh.combine(g1,g2)
        fig=plt.figure()
        axs=fig.subplots(4,1)
        g1.draw_matplotlib(axs[0])
        g2.draw_matplotlib(axs[1])
        g_res.draw_matplotlib(axs[2])
        g_ref.draw_matplotlib(axs[3])
        fig.savefig('figure.pdf')
        self.assertEqual(
            g_res,
            g_ref
        )
