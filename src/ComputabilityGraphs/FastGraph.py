from typing import FrozenSet
from ComputabilityGraphs.graph_helpers import equivalent_singlegraphs
import networkx as nx
from frozendict import frozendict
from functools import reduce
from .TypeSynonyms import Node, Decomp, Computer, ComputerSet
from .helpers import merge_dicts
from .graph_plotting import varset_2_string, varsettuple_2_string, compset_2_string
from . import graph_helpers as gh

class FastGraph:
    '''This class represents a special kind of bipartite graph 
    and delegates most of its methods to its internal nx.DiGraph instance'''
    def __init__(self):
        dg = nx.DiGraph()
        self.dg = dg


    def get_Nodes(self):
        dg = self.dg
        try:
            sets = frozenset({n for n, d in dg.nodes(data=True) if d["bipartite"] == 0})
        except:
            from IPython import embed;embed()

        return sets

    def get_Decomps(self):
        return frozenset({n for n, d in self.dg.nodes(data=True) if d["bipartite"] == 1})

   # def src_nodes_computerset_tuples(
   #         self,
   #         n: Node 
   #     )->FrozenSet[Tuple[Node,ComputerSet]]
   #     """Return set of tuples 
   #     Since FastGraph is internally bibartite, vvery node has 
   #     a the direct predecessors of a node are decompositions.
   #     Every decomposition has a node as predecessor to which
   #     s1 = frozenset([tC.A])
   #     s2 = frozenset([tC.B])
   #     n = frozenset.union(s1,s2)
   #     d = (s1,s2) 
   #     g.add_Node(n)
   #     g.add_Decomp(targetNode=n,decomp=d)
   #     it is connected via a set of computersets.
   #     This function returns the src nodes along wiht the 
   #     computersets leading to the target_node (via the 
   #     decompositions). The function is needed for the projection
   #     of the bipartite graph onto the directed multigraph that
   #     consists only of Nodes."""
   #         
   #     def f(acc,el):
   #         decomp,_ = el
   # 
   #         computersets = reduce(get_computersets_from_decomp, decomps)
   #          
   #     tuples = reduce(
   #         f,
   #         self.dg.in_edges()
   #     )
    def in_edges(self,*args,**kwargs):
        return self.dg.in_edges(*args,**kwargs)

    def get_edge_data(self,*args,**kwargs):
        return self.dg.get_edge_data(*args,**kwargs)
        
    def add_Node(
            self,
            node: Node
        ):
        self.dg.add_node(node, bipartite=0)

    def has_Decomp(
            self,
            decomp: Decomp
        ) -> bool:
        return decomp in self.get_Decomps()

    def add_Decomp(
            self,
            targetNode: Node,
            decomp: Decomp
        ):
        dg = self.dg
        dg.add_node(decomp, bipartite=1)
        dg.add_edge(decomp, targetNode)

    def add_edge(self,s,t,**kwargs):
        self.dg.add_edge(s,t,**kwargs)

    def has_edge(self, s, t) -> bool:
        return self.dg.has_edge(s,t)
    

    def __eq__(self,other):
        return gh.equivalent_singlegraphs(self.dg,other.dg)

    def draw_matplotlib(
            self,
            ax,
            mvar_aliases=frozendict({}),
            computer_aliases=frozendict({}),
            targetNode=None,
            pos=None,
            **kwargs
    ):
        spsg = self.dg
        #top_nodes = frozenset({n for n, d in spsg.nodes(data=True) if d["bipartite"] == 0})
        top_nodes = self.get_Nodes()
        #bottom_nodes = frozenset( set(spsg) - top_nodes )
        bottom_nodes = self.get_Decomps()
        set_labels = {n: varset_2_string(n, mvar_aliases) for n in top_nodes}
        decomp_labels = {n: varsettuple_2_string(n, mvar_aliases) for n in bottom_nodes}
        labels = merge_dicts(set_labels, decomp_labels)
        if pos is None:
            # layout alternatives
            pos = nx.spring_layout(spsg)
            # pos = nx.circular_layout(spsg)
            # pos = nx.spring_layout(spsg, iterations=20)
            # pos = nx.circular_layout(spsg )
            ##pos = nx.kamada_kawai_layout(spsg) #funny artefacts
            # pos = nx.planar_layout(spsg)
            # pos = nx.random_layout(spsg)
            # pos = nx.shell_layout(spsg)
            # pos = nx.spectral_layout(spsg)
            # pos = nx.spiral_layout(spsg)
        
        nx.draw_networkx_labels(
            spsg,
            labels=labels,
            ax=ax,
            font_color='black',
            pos=pos,
            **kwargs
        )
        nx.draw_networkx_edges(
            spsg,
            #labels=labels,
            ax=ax,
            pos=pos,
        )
        nx.draw_networkx_nodes(
            spsg,
            ax=ax,
            pos=pos,
            node_size=1000,
            nodelist=list(top_nodes),
            node_color='orange',
            alpha=0.8
        )
        nx.draw_networkx_nodes(
            spsg,
            ax=ax,
            pos=pos,
            nodelist=list(bottom_nodes),
            node_color='g',
            alpha=0.8
        )
        if targetNode is not None:
            res = minimal_startnodes_for_node(spsg, targetNode)
            nx.draw_networkx_nodes(
                spsg,
                pos,
                nodelist=[targetNode],
                node_color='r',
                alpha=0.8
            )
            nx.draw_networkx_nodes(
                spsg,
                pos,
                nodelist=list(res),
                node_color='r',
                alpha=0.4
            )
    
        ax.axis("On")
    
        # at the moment it is not possible to draw
        # more than one edge (egde_lables) between nodes
        # directly (no edgelabels for MultiDiGraphs)
        # therefore we draw only one line for all computersets
        def edgeDict_to_string(ed):
            target = "computer_sets"
            if target in ed.keys():
                comp_sets=ed[target]
                comp_set_strings= [compset_2_string(cs, computer_aliases) for cs in comp_sets]
                res = "\n".join(comp_set_strings)
            else:
                res=''
            return res 
    
        edge_labels = {e: edgeDict_to_string(spsg.get_edge_data(*e)) for e in spsg.edges()}
    
        nx.draw_networkx_edge_labels(spsg, ax=ax, edge_labels=edge_labels, pos=pos)
        mvar_aliases_inv = {val: key for key, val in mvar_aliases.items()}
        for i, k in enumerate(sorted(mvar_aliases_inv.keys())):
            ax.text(0, 0 - i / len(mvar_aliases), k + ": " + mvar_aliases_inv[k])
    
        

