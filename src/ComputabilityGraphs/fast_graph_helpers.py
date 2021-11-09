from functools import lru_cache, reduce
import networkx as nx
import time
import matplotlib.pyplot as plt
from matplotlib.colors import CSS4_COLORS, BASE_COLORS, TABLEAU_COLORS
from pygraphviz.agraph import AGraph
from typing import List, Set, Tuple, Callable, FrozenSet
from copy import deepcopy
from frozendict import frozendict

from .TypeSynonyms import  Computer
from . import helpers as h
from .str_helpers import nodes_2_string
from .FastGraph import  FastGraph
from .Decomposition import Decomposition
from .Node import Node
from .ComputerSet import ComputerSet

def combine(
        g1: FastGraph,
        g2: FastGraph
    ):
    css_key = g1.__class__.css_key
    g=deepcopy(g1)
    for node in g2.get_Nodes():
        g.add_Node(node)

    for decomp in g2.get_Decomps():
        g.add_unconnected_Decomp(decomp)

    for (src,target,edge_dict) in g2.dg.edges(data=True):
        if type(src) == Node and type(target)==Decomposition and css_key in edge_dict.keys():
                g.connect_Node_2_Decomposition(
                        node=src,
                        target_decomp=target,
                        computer_sets=edge_dict[css_key]
                )
        else: #if type(src)==Decomposition and type(target)==Node: 
                g.connect_Decomposition_2_Node(
                        decomp=src,
                        target_node=target
                )

    return g

def src_node_computersets_tuples_from_decomp(
        g: FastGraph,
        d: Decomposition
    )->FrozenSet[Tuple[Node,ComputerSet]]:
    # This functions is necessary for the projection of the FastGraph
    # to the MultiDiGraphs containing no Decomps but only nodes but
    # preserving the information contained in the edges
    # it collects all the src nodes and computersets of one decompositon
    def f(acc,e):
        src,_ = e
        css = g.get_edge_data(src,d)['computer_sets'] 
        tup =(src,css)
        return acc+[(src,css)]

    l = reduce(f,g.in_edges(d),[])
    return frozenset(l) 

def src_node_computersets_tuples_from_node(
        g: FastGraph,
        n: Node
    )->FrozenSet[Tuple[Node,ComputerSet]]:
    # This functions is necessary for the projection of the FastGraph
    # to the MultiDiGraphs containing no Decomps but only nodes but
    # preserving the information contained in the edges
    # It collects all the src nodes and computersets of a node, collecting
    # them for all decompositions of this node
    def f(acc,e):
        src,_ = e
        ld= list(src_node_computersets_tuples_from_decomp(g,src))
        return acc+ld

    l = reduce(f,g.in_edges(n),[])
    return frozenset(l) 


def project_to_multiDiGraph(fg):
    ns = fg.get_Nodes()
    g=nx.MultiDiGraph()
    g.add_nodes_from(ns)


    def f(g,n):
        gf = deepcopy(g)
        tups = src_node_computersets_tuples_from_node(fg,n)
        def h(g,tup):
            src, computersets = tup
            gh=deepcopy(g)
            def j(g,cs):
                gj=deepcopy(g)
                gj.add_edge(src,n,computers=cs)
                return gj

            return reduce(j,computersets,gh)

        return reduce(h,tups,gf)


    return reduce(f,ns,g)

def add_combi_arg_set_graph(
        g: FastGraph,
        root: Node,
        decomp: Decomposition,
        computer_combi: Set[Computer]
) -> Tuple[
    FastGraph,
    FrozenSet[Node]
]:
    _, passive = decomp
    args = reduce(frozenset.union,[h.arg_set(computer) for computer in computer_combi],frozenset())
    arg_node = frozenset.union(args,passive)
    avoid_nodes = g.visited_Nodes_on_paths(
        src=decomp,
        root=root
    )
    if any([arg_node.issuperset(avn) for avn in avoid_nodes]):
        return (g,frozenset())
    else:
        e = (arg_node, decomp)
        # A situation arising from combis like {a(c),b(d)} and {b(c),a(d)}
        G = deepcopy(g)
        if G.has_edge(*e):
            key = 'computer_sets'
            # fixme mm 8-21-2021 
            data = G.get_edge_data(*e)[key]
            G.get_edge_data(*e)[key] =frozenset.union(data,frozenset({computer_combi}))
            return (G, frozenset())
        else:
            G.add_Node(arg_node)
            # if edge does not exist
            G.add_edge(arg_node, decomp, computer_sets=frozenset([computer_combi]))
            return (G, frozenset({arg_node}))


def add_combis_arg_set_graphs_to_decomp(
        g: FastGraph,
        root: Node,
        decomp: Decomposition,
        computer_combis: FrozenSet[ComputerSet]
) -> Tuple[
    FastGraph,
    FrozenSet[Node]
]:
    def f(acc, el):
        g, new_nodes = acc
        computer_combi = el
        g_new,combi_new_nodes = add_combi_arg_set_graph(g, root, decomp, computer_combi)
        new_nodes = frozenset.union(new_nodes, combi_new_nodes)
        return(g_new, new_nodes)

    return reduce(f, computer_combis, (g, frozenset()))


def add_all_arg_set_graphs_to_decomp(
        g: FastGraph,
        root: Node,
        decomp: Decomposition,
        all_computers
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:  
    g_new = deepcopy(g)
    active, passive = decomp
    # we want to avoid all the nodes on the path from here to the root Node
    avoid_nodes= g.visited_Nodes_on_paths(
            src=decomp,
            root=root
    )
    all_combies = h.all_computer_combis_for_mvar_set(
            var_set=active,
            all_computers=all_computers,
            avoid_nodes=avoid_nodes
    )

    def src2node(ss):
        return frozenset.union(ss, passive)

    src_sets = frozenset(map(h.combi_arg_set, all_combies))
    # we want to add only nodes that are not supersets of other nodes (we are
    # interested in a SPARSE graph) but if a computercombi creates a new egde
    # to an EXISTING node we want to add the edge and therefore have to include
    # the combi in the call to add_combis_arg_set_graphs_to_decomp
    src_sets_wo_ss = h.remove_supersets(src_sets)
    src_nodes_wo_ss = frozenset(map(src2node, src_sets_wo_ss))
    #super_sets = frozenset.difference(src_sets, src_sets_wo_ss)
    #print("supersets="+nodes_2_string(super_sets))
    #super_set_nodes = frozenset(map(src2node, super_sets))
    #super_set_nodes_already_in_g = frozenset.intersection(
    #    g_new.get_Nodes(),
    #    super_set_nodes
    #)
    #print("super_set_nodes_alreay_in_G="+nodes_2_string(super_set_nodes_already_in_g))

    relevant_nodes = frozenset.union(
        #super_set_nodes_already_in_g,
        src_nodes_wo_ss
        #frozenset(map(src2node, src_sets))
    )
    relevant_combis = frozenset(
        filter(
            lambda combi: src2node(h.combi_arg_set(combi)) in relevant_nodes,
            all_combies
        )
    )

    return add_combis_arg_set_graphs_to_decomp(
                g_new,
                root,
                decomp,
                relevant_combis
            )


def add_arg_set_graphs_to_decomps(
        g: nx.DiGraph,
        root: Node,
        decomps: Set[Decomposition],
        all_computers: FrozenSet[Computer]
) -> Tuple[
    nx.DiGraph,
    FrozenSet[Node]
]:
    def f(acc, decomp):
        print(decomp)
        g, new_nodes = acc
        active, passive = decomp
        g_new, combi_new_nodes = add_all_arg_set_graphs_to_decomp(
                g,
                root,
                decomp,
                all_computers
        )

        new_nodes = frozenset.union(new_nodes, combi_new_nodes)
        return(g_new, new_nodes)

    return reduce(f, decomps, (g, frozenset()))

def prospective_decomp_list(node,uncomputable):
    actives = h.power_set(node)
    return [
        Decomposition(active=Node(a),passive=Node(frozenset.difference(node,a))) 
        for a in actives 
        if len(frozenset.intersection(a, uncomputable)) == 0 and len(a) != 0
    ]

def prospective_decomp_list_2(
        node: Node,
        passive: FrozenSet[Node]
    ):
    # instead of uncomputable variables we use a more general set of 
    # uncomputable Nodes
    allowed_actives = [ 
        a for a in h.power_set(node) 
        if not any([a.issuperset(p) for p in passive]) and
        a != Node([])
    ]

    return [
        Decomposition(active=Node(a),passive=Node(frozenset.difference(node,a))) 
        for a in allowed_actives 
    ]

def add_all_decompositions_to_node(
        g: FastGraph,
        node: Node,
        passive: FrozenSet[Node],
    ) -> Tuple[FastGraph, FrozenSet[Decomposition]]:
    

    decompositions_2 = prospective_decomp_list_2(node,passive)
    if len(decompositions_2) == 0:
        return g, frozenset([])

    new_decompositions = frozenset(filter(lambda d: not(g.has_Decomp(d)), decompositions_2))
    for d in decompositions_2:
        g.add_Decomp(node,d)

    return (g, new_decompositions)

def add_all_decompositions_to_all_nodes(
        g: FastGraph,
        root: Node,
        nodes: FrozenSet[Node],
        uncomputable: FrozenSet[type]
        ) -> Tuple[FastGraph, FrozenSet[Decomposition]]: 
    g_new = deepcopy(g)
    def f(acc, node):
        g, decompositions = acc
        # we want to avoid Decompostions with active parts containing 
        # variables that have been in the passive parts of decompositions on 
        # our path(s) to the starting point.
        # In other words decompositions are branchings that should stay in effect
        # for all the following branchings. If we decide that {C} is considered
        # passive and not to be resolved in one decomposition we want all future 
        # decompositions to treat it as such and include it in the uncomputables
        
        res_p = g.passive_Nodes_in_Decompositions_on_paths(
            src=node,
            root=root
        )
        passive=frozenset.union(
            frozenset([n for n in res_p if n!=Node({})]), 
            frozenset([Node({v}) for v in uncomputable])
        )





        g_new, node_decomps = add_all_decompositions_to_node(
            g, 
            node, 
            passive=passive
        )
        new_decompositions = frozenset.union(
            decompositions,
            node_decomps
        )
        return g_new, new_decompositions

    g_res, all_new_decompositions = reduce(
        f,
        nodes,
        (g_new, frozenset())
    )
    return g_res, all_new_decompositions


@lru_cache
def fast_graph(
        root_type: type,
        cs: ComputerSet,
        given: FrozenSet[type]
    ) -> FastGraph:    
    g,new_nodes = last(update_generator(
        root_type,
        cs,
        max_it=30,
        given=given
    ))
    return g


def last(iterator):
    return reduce(lambda acc,el:el,iterator)

def update_generator(
        root_type: type,
        cs: ComputerSet,
        max_it: int,
        given: FrozenSet[type] = frozenset()
    ) -> 'generator':
    
    if max_it < 0:
        raise IndexError("update sequence indices have to be larger than 0")
    uncomputable = frozenset.union(
            h.uncomputable(cs),
            given
    )
    print('uncomputable='+h.node_2_string(uncomputable))
    
    g, ds= initial_fast_graph(
        root_type=root_type,
        cs=cs
    )
    yield (g, ds)
    counter = 1

    while True:
        print(counter)
        # first halfstep
        g, ns = add_arg_set_graphs_to_decomps(g, Node({root_type}),ds, cs)
        print('new_nodes='+nodes_2_string(ns))
        if ((len(ns) == 0) or (counter > max_it)):
            break
        yield (g, ns)
        counter += 1
        
        # second halfstep
        g, ds = add_all_decompositions_to_all_nodes(
            g,
            Node({root_type}),
            ns,
            uncomputable=uncomputable
        )
        if ((len(ds) == 0) or (counter > max_it)):
            break
        yield (g, ds)
        counter += 1

    
def initial_fast_graph(
        root_type: type,
        cs: ComputerSet
) -> FastGraph:
    root = Node({root_type}) 
    g = FastGraph()
    g.add_Node(root)
    new_decompositions = frozenset(
        [
            Decomposition(
                active=root,
                passive=Node([])
            ) 
        
        ]
    ) if root_type not in h.uncomputable(cs) else frozenset()
    for dn in new_decompositions:
        g.add_Decomp(dn[0], dn)

    return g, new_decompositions 
    
def add_passive(sg,p):
    d2nes = [(s,t) for  (s,t) in sg.dg.edges if sg.dg.nodes[t]['bipartite']==0]
    n2des = [
            (s,t,d) 
            for  (s,t,d) in sg.dg.edges(data=FastGraph.css_key)
            if sg.dg.nodes[t]['bipartite']==1
    ]
    
    tsg = FastGraph()
    # in case we have unconnected nodes in sg (e.g. single node graphs 
    for t in sg.get_Nodes():
        tp = t.add_passive(p)
        tsg.add_Node(tp)
    
    for (s,t) in d2nes:
        sp = s.add_passive(p)
        tp = t.add_passive(p)
        #tsg.add_Node(tp)
        tsg.add_Decomp(decomp=sp,targetNode=tp)
        
    for (s,t,css) in n2des:
        sp = s.add_passive(p)
        tp = t.add_passive(p)
        tsg.add_connected_Node(
            node=sp,
            target_decomp=tp,
            computer_sets=css
        )

    return tsg

def draw_update_sequence(
        root_type: type,
        computers: ComputerSet,
        max_it: int,
        fig: plt.figure,
        given: FrozenSet[type] = frozenset(),
        mvar_aliases=frozendict({}),
        computer_aliases=frozendict({})
    ):
    lg = [
        g for (g,new) 
        in update_generator(
            root_type,
            computers,
            max_it,
            given
        )
    ]
    print(type(lg[-1]))
    nr = len(lg)
    fig.set_size_inches(20, 20 * nr)
    #pos = nx.spring_layout(lg[-1].dg)
    # layout alternatives
    pos = nx.spring_layout(
        lg[-1].dg,
        scale=10,
        fixed=None,
        dim=2
    )
    #pos = nx.circular_layout(lg[-1].dg )
    #pos = nx.kamada_kawai_layout (lg[-1].dg,scale=2)
    #pos = nx.planar_layout (lg[-1].dg)
    #pos = nx.random_layout (lg[-1].dg)
    #pos = nx.shell_layout (lg[-1].dg)
    #pos = nx.spectral_layout (lg[-1].dg)
    #pos = nx.spiral_layout (lg[-1].dg)
    axs = fig.subplots(nr, 1, sharex=True, sharey=True)
    for i in range(nr):
        lg[i].draw_matplotlib(
            axs[i],
            mvar_aliases,
            computer_aliases,
            pos=pos
        )
