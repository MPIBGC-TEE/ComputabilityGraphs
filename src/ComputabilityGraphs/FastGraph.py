import networkx as nx
from typing import FrozenSet
from copy import deepcopy
from frozendict import frozendict
from functools import reduce
from pygraphviz.agraph import AGraph
from .TypeSynonyms import Node, Decomp, Computer
from .Decomposition import Decomposition
from .ComputerSet import ComputerSet
from .helpers import ( 
    equivalent_singlegraphs,
    merge_dicts,
    varset_2_string,
    varsettuple_2_string,
    compset_2_string
)

class FastGraph:
    '''This class represents a special kind of bipartite graph 
    and delegates most of its methods to its internal nx.DiGraph instance'''
    # class variable
    css_key='computer_sets'

    def __init__(self):
        dg = nx.DiGraph()
        self.dg = dg

    def root(self):
        dg=self.dg
        end_nodes = [n for n in  dg.nodes() if dg.out_degree(n)==0]
        l = len(end_nodes)
        if l > 1:
            raise Exception("more than one target node")
        if len == 0:
            raise Exception("no target nodes")

        return end_nodes[0]
        

    def __hash__(self):
        dg=self.dg
        return hash(
            (
                frozenset(dg.nodes()),
                frozenset(dg.edges())
            )
        )

    def __str__(self):
        css_key = self.__class__.css_key
        return "\n".join(
            [
                str(s) + '-' +str(d[css_key]) + '->' + str(t) if css_key in d.keys() 
                else str(s) + '->' + str(t) 
                for (s, t, d) in self.dg.edges(data=True)
            ]
        ) 


    def passive_Nodes_in_Decompositions_on_paths(
            self,
            src: Node,
            root: Node
        )-> FrozenSet[Node]:

        paths = nx.shortest_simple_paths(
            self.dg,
            source=src,
            target=root
        )
        # the result is a generator of node lists
        # from every node list we extract the Decompositions
        # and from every Decomposition the passive part
        dg = self.dg
        def decomps_from_nodelist(node_list):
            return [ 
                n for n in node_list
                if 'bipartite' in dg.nodes[n].keys() and 
                dg.nodes[n]['bipartite']==1
                
            ]
        
        def passive_Nodes_list(path):
            ds = decomps_from_nodelist(path)
            return [ d.passive for d in ds]

        return frozenset(
            reduce(
                lambda acc,pl: acc + pl,
                map(passive_Nodes_list,paths)
            )
        )

    def visited_Nodes_on_paths(
            self,
            src: Decomposition,
            root: Node
        )-> FrozenSet[Node]:

        paths = nx.shortest_simple_paths(
            self.dg,
            source=src,
            target=root
        )
        # the result is a generator of node lists
        # from every node list we extract the Decompositions
        # and from every Decomposition the passive part
        dg = self.dg
        def previous_nodes_nodelist(node_list):
            return [ 
                n for n in node_list
                if 'bipartite' in dg.nodes[n].keys() and 
                dg.nodes[n]['bipartite']==0
                
                ] 
        
        return frozenset(
            reduce(
                lambda acc,pl: acc + pl, # combine the lists of the different paths
                map(previous_nodes_nodelist,paths)
            )
        )

    def get_Nodes(self):
        dg = self.dg
        try:
            sets = frozenset({n for n, d in dg.nodes(data=True) if d["bipartite"] == 0})
        except:
            sets = frozenset() 

        return sets

    def get_Decomps(self):
        k="bipartite"
        return frozenset({n for n, d in self.dg.nodes(data=True) if k in d.keys() and d[k] == 1})

    def in_edges(self,*args,**kwargs):
        return self.dg.in_edges(*args,**kwargs)

    def get_edge_data(self,*args,**kwargs):
        return self.dg.get_edge_data(*args,**kwargs)
        
    def add_Node(
            self,
            node: Node
        ):
        self.dg.add_node(node, bipartite=0)

    def add_connected_Node(
            self,
            node: Node,
            target_decomp: Decomposition,
            computer_sets: FrozenSet[ComputerSet]
        ):
        self.add_Node(node)
        self.add_edge(
            node,
            target_decomp,
            computer_sets=computer_sets
        )
        
    def connect_Node_2_Decomposition(
            self,
            node,
            target_decomp,
            computer_sets
        ):
        if not self.has_edge(node,target_decomp): 
            self.add_connected_Node(
                node=node,
                target_decomp=target_decomp,
                computer_sets=computer_sets
            )
        else:
            css_key= self.__class__.css_key
            css = self.dg[node][target_decomp][css_key]
            css = frozenset.union(css,computer_sets)
    
    def connect_Decomposition_2_Node(
            self,
            decomp,
            target_node
        ):
        if not self.has_edge(decomp,target_node): 
            self.add_edge(decomp,target_node)


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
    
    def add_unconnected_Decomp(
            self,
            decomp: Decomp
        ):
        dg = self.dg
        dg.add_node(decomp, bipartite=1)




    def add_edge(self,s,t,computer_sets=None,**kwargs):
        self.dg.add_edge(s,t,**kwargs)
        if computer_sets is not None:
            self.dg[s][t][self.__class__.css_key]=computer_sets

    def has_edge(self, s, t) -> bool:
        return self.dg.has_edge(s,t)
    

    def __eq__(self,other):
        return equivalent_singlegraphs(self.dg,other.dg)

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
            target = self.__class__.css_key
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
    
        

    def to_AGraph(
            self,
            mvar_aliases=frozendict({}),
            computer_aliases=frozendict({}),
            targetNode=None,
            pos=None,
            **kwargs
    ):
        nodes = self.get_Nodes()
        decomps = self.get_Decomps()
        A = AGraph(directed=True)
        A.node_attr["style"] = "filled"
        A.node_attr["shape"] = "rectangle"
        A.node_attr["fixedsize"] = "false"
        A.node_attr["fontcolor"] = "black"

        for node in nodes:
            A.add_node(varset_2_string(node, mvar_aliases),color='orange')

        for node in decomps:
            A.add_node(varsettuple_2_string(node, mvar_aliases),color='green')

        edges = self.dg.edges(data=True)
        for edge in edges:
            s, t, data_dict = edge
            if s in nodes: 
                computer_sets = data_dict["computer_sets"]
                ss = varset_2_string(s, mvar_aliases)
                st = varsettuple_2_string(t, mvar_aliases)
                for cs in computer_sets:
                    for c in cs:
                        A.add_edge(ss, st)
                        Ae = A.get_edge(ss, st)
                        #Ae.attr["color"] = cf(c)
                        #Ae.attr["fontcolor"] = cf(c)
                        Ae.attr["label"] = c.__name__
            else:
                ss = varsettuple_2_string(s, mvar_aliases)
                st = varset_2_string(t, mvar_aliases)
                A.layout('circo')
                A.add_edge(ss, st)
        return A
