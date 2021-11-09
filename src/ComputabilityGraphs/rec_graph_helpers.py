from functools import reduce, lru_cache
from typing import FrozenSet
from copy import deepcopy
from . import helpers as h
from . str_helpers import nodes_2_string
from . import  fast_graph_helpers as fgh
from .FastGraph import FastGraph
from .Decomposition import Decomposition
from .Node import Node
from .ComputerSet import ComputerSet



def rec_graph_maker(computers):
    # we create a pair of recursive functions that call each other
    uncomputable=h.uncomputable(computers)

    @lru_cache
    def decomp_graph(
            decomposition,
            avoid_nodes,
            given=frozenset()
        ):
        a,p=decomposition
        if any(
            [
                a.issuperset(an) 
                for an in avoid_nodes
            ]
        ):
            print("###############################","this should not happen")
            return FastGraph()
        else:

            all_combies = h.all_computer_combis_for_mvar_set(
                    a,
                    computers,
                    avoid_nodes
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
            #print("supersets="+nodes_2_string(super_sets))


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
                        ),
                        given=given
                    ) 
                )
                for (combi_set,arg_set) in combiset_argset_tups 
            ]
        

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
            
            return dg

    ################################################
    ################################################
    ################################################

    @lru_cache
    def node_graph(
            g,
            prospective_start_nodes,
            avoid_nodes,
            given: FrozenSet[type]=frozenset()
        ):
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
        # define halting conditions
        
        if len(allowed_start_nodes) == 0:
            # case 1.
            # We are out of options to investigate further.  So we are done and
            # return the unchanged graph.
            return g #,frozenset())
        
        elif len(allowed_start_nodes) == 1:
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
            # - if at least one of the decompositions leads a new subgraph we will add the
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
                    frozenset.union(
                        uncomputable,
                        given
                    )
            )

            d_subgraphs_tuples = [
                (
                    d,
                    decomp_graph(
                        decomposition=d,
                        avoid_nodes=avoid_nodes,
                        given=given
                    ) 
                )
                for d in computable_decomps
            ]

            dg = FastGraph()
            dg.add_Node(start_node)
            def f(sg,t):
                d,tsg = t
                sg = deepcopy(sg)
                sg = fgh.combine(sg,tsg)
                sg.connect_Decomposition_2_Node(decomp=d,target_node=start_node)
                return sg
                
            dgg = reduce(
                f,
                filter(
                    lambda t: len(t[1].get_Nodes()) >0,
                    d_subgraphs_tuples
                ),
                dg
            )
            for e in dgg.dg.edges:
                s,t=e

            g = fgh.combine(g,dgg)
            for e in g.dg.edges:
                s,t=e

            return g

    return (decomp_graph, node_graph)

    
@lru_cache
def fast_graph(
        cs: ComputerSet,
        root_type: type ,
        given: FrozenSet[type]=frozenset()
):
    # wrapper to create the same interface as the fast_graph function in fast_graph_helpers
    # which works differently 
    _, node_graph = rec_graph_maker(cs) 
    sn = Node([root_type])
    return node_graph(
            FastGraph(),
            prospective_start_nodes=frozenset({sn}),
            avoid_nodes=frozenset(),
            given=given
    )


