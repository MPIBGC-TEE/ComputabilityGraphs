from functools import reduce
from copy import deepcopy
from . import helpers as h
from . import  fast_graph_helpers as fgh
from .FastGraph import FastGraph
from .Decomposition import Decomposition
from .Node import Node



def rec_graph_maker(computers):
    # we create a pair of recursive functions that call each other
    uncomputable=h.uncomputable(computers)
    def decomp_graph(
            decomposition,
            avoid_nodes
        ):
        print('########### in decomp_graph #############')
        print('decomp_graph decompostion: ',decomposition)
        print('decomp_graph avoid_nodes: ',h.nodes_2_string(avoid_nodes))
        a,p=decomposition
        if any(
            [
                a.issuperset(an) 
                for an in avoid_nodes
            ]
        ):
            return FastGraph()
        else:

            all_combies = h.all_computer_combis_for_mvar_set(
                    a,
                    computers
            )
            # arg_set
            tups = [(c, Node(h.combi_arg_set(c))) for c in all_combies]
            # we can filter out reduntant combis (computersets)
            # that lead to more dependencies than others
            # this should save some time later when the sub graphs
            # have to be combined 
            # it is also possible that two computersets have the same
            #src_sets = frozenset([a for (c,a) in tups])
            #src_sets_wo_ss = h.remove_supersets(src_sets)
            #super_sets = frozenset.difference(src_sets, src_sets_wo_ss)
            #print("supersets="+h.nodes_2_string(super_sets))

            #def combis(arg_set):
            #    return frozenset([c for (c,a) in tups if a==arg_set]) 

            #combiset_argset_tups =[(combis(a),a) for a in src_sets_wo_ss]
            combiset_argset_tups =[(frozenset([c]),a) for (c,a) in tups]
            
            # now make a subgraph for every src_set
            cs_node_subgraphs_tuples = [
                (
                    combi_set,
                    arg_set,
                    node_graph(
                        FastGraph(),
                        prospective_start_nodes=frozenset([arg_set]),
                        avoid_nodes=frozenset.union(
                            avoid_nodes,
                            Node([a])
                        )
                    ) 
                )
                for (combi_set,arg_set) in combiset_argset_tups 
            ]
        
            print('########### back in decomp_graph #############')
            #for t in node_subgraphs_tuples:
            #    n,g = t
            #    print('node: ',n)
            #    print('g nodes: ',h.nodes_2_string(g.get_Nodes()))
            #    print('g decomps: ',h.decompositions_2_string((g.get_Decomps())))

            def empty_subgraph_tup(tup):
                combi_set,arg_set,sg =tup
                return len(sg.get_Nodes()) > 0

            relevant_tups = list(filter(
                empty_subgraph_tup,
                cs_node_subgraphs_tuples
            ))

            dg = FastGraph()
            if len(relevant_tups) > 0:
                dg.add_unconnected_Decomp(decomposition)

                def f(dg,t):
                    css, n, sg = t
                     
                    tsg=fgh.add_passive(sg,p)
                    dg = fgh.combine(dg,tsg)
                    dg.add_connected_Node(
                            node=n.add_passive(p),
                            target_decomp=decomposition,
                            computer_sets=css
                    )
                    return dg
                    
                dg = reduce(f, relevant_tups, dg)
            
            print('dg nodes: ',h.nodes_2_string(dg.get_Nodes()))
            print('dg decomps: ',h.decompositions_2_string((dg.get_Decomps())))
            return dg

    ################################################
    ################################################
    ################################################

    def node_graph(
            g,
            prospective_start_nodes,
            avoid_nodes
        ):
        print('########### in node_graph #############')
        g = deepcopy(g)
        allowed_start_nodes = [
            n for n in prospective_start_nodes
            if not(
                any(
                    [
                        n.issuperset(an) 
                        for an in avoid_nodes
                    ]
                )
            )
            
        ]
        print('prospective_start_nodes: ',h.nodes_2_string(prospective_start_nodes))
        print('avoid_nodes: ',h.nodes_2_string(avoid_nodes))
        print('start_nodes: ',h.nodes_2_string(allowed_start_nodes))
        print('len(start_nodes): ',len(allowed_start_nodes))
        # define halting conditions
        
        if len(allowed_start_nodes) == 0:
            # case 1.
            # We are out of options to investigate further.  So we are done and
            # return the unchanged graph.
            print("graph cannot be extended")
            return g #,frozenset())
        
        elif len(allowed_start_nodes) == 1:
            print("case 2")
            # case 2
            # we have one start_node whose 
            # computable_decomps we can explore.
            # In every case we will  remove this starting_point after having explored it.
            # The exploration has two possible outcomes:
            # - if none of the computable_decomps
            #   leads to a new graph we will return
            #   the same graph but with no new start_nodes, which will lead to
            #   an end of the recursion in the next recursive call (case 1)
            #
            # - if at least one of the decomposition leads a new subgraph we will add the
            #   subgraph to the present graph and report it's starting point as a
            #   prospective starting point and in the next recursive call might
            #   end up in this case 2 again.
            #
            start_node = allowed_start_nodes[0]
            
            
            
            #avoid_nodes=frozenset.union(
            #        avoid_nodes,
            #        Node([start_node])
            #)
            
            computable_decomps = fgh.prospective_decomp_list(
                    start_node,
                    uncomputable
            )
            print(
                "computable_decomps: ",
                h.decompositions_2_string(computable_decomps)
            )

            d_subgraphs_tuples = [
                (
                    d,
                    decomp_graph(
                        decomposition=d,
                        avoid_nodes=avoid_nodes
                    ) 
                )
                for d in computable_decomps
            ]
            print("########### back in node_graph ##########")
            for t in d_subgraphs_tuples:
                d,g = t
                print('decomposition: ', d)
                print('g nodes: ', h.nodes_2_string(g.get_Nodes()))
                print('g decomps: ', h.decompositions_2_string((g.get_Decomps())))

            dg = FastGraph()
            dg.add_Node(start_node)
            def f(sg,t):
                d,tsg = t
                sg = deepcopy(sg)
                sg = fgh.combine(sg,tsg)
                sg.connect_Decomposition_2_Node(decomp=d,target_node=start_node)
                #if len(tsg.get_Nodes()) > 0:
                #    #sg.add_Decomp(decomp=d,targetNode=start_node)
                #    print('start_node:',start_node)
                #    print('d:',d)
                #    sg = fgh.combine(sg,tsg)
                #    sg.connect_Decomposition_2_Node(decomp=d,target_node=start_node)
                return sg
                
            dgg = reduce(
                f,
                filter(
                    lambda t: len(t[1].get_Nodes()) >0,
                    d_subgraphs_tuples
                ),
                dg
            )
            print('dg nodes: ',h.nodes_2_string(dg.get_Nodes()))
            for e in dgg.dg.edges:
                s,t=e
                print('dg edges: ','('+str(s)+','+str(t)+')')

            g = fgh.combine(g,dgg)
            print('g nodes: ',h.nodes_2_string(g.get_Nodes()))
            for e in g.dg.edges:
                s,t=e
                print('g edges: ','('+str(s)+','+str(t)+')')

            return g

    return (decomp_graph, node_graph)

    
    


