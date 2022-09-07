#from .ComputerSet import ComputerSet
from typing import List, Dict, Callable, Set
from functools import lru_cache, reduce, _lru_cache_wrapper
from inspect import signature
from copy import copy
import ComputabilityGraphs.helpers as h
import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.function import edges
from networkx.algorithms import bipartite
from ipywidgets import Layout, Button, Box, VBox, Label, HTMLMath, Output

from . import helpers as h
class BiGraph(nx.DiGraph):
    def computer_names(self):
        def translate(c):
            return c.__wrapped__.__name__ if isinstance(c,_lru_cache_wrapper) else str(c)

        computers, _ = bipartite.sets(self)
        return [translate(c) for c in computers]

    def types(self):
        _ , types = bipartite.sets(self)
        return types

    def type_names(self):
        return [t.__name__ for t in self.types()]

    def target_type(self):
        return [n for n in self.nodes if self.out_degree(n)==0][0]



    def draw_matplotlib(
            self, 
            ax, 
            pos=None,
            given=frozenset(),
            computer_aliases=None,
            type_aliases=None
        ):

        target_node=self.target_type()
        computers, types = bipartite.sets(self)
        pos=nx.bipartite_layout(self, types) #if pos is None else pos
        font_size=20
        # plot given types
        if type_aliases is None or computer_aliases is None:
            ax.plot(-1,0)
            ax.plot(2,0)
            font_size=0.7*font_size
            #pos={k:0.1*v for k,v in pos.items()}
        
        given_and_present = given.intersection(self.types())
        nx.draw_networkx_nodes(
            G=self,
            pos=pos,
	    ax=ax,
	    nodelist=given_and_present,
	    node_color="green",
            alpha=0.3,
            label="given"
        )
        # plot missing types
        nx.draw_networkx_nodes(
            G=self,
            pos=pos,
	    ax=ax,
	    nodelist=types.difference(given),
	    node_color="red",
            alpha=0.3,
            label="missing"
        )

        if type_aliases is None:
            type_labels={t:t.__name__ for t in types}
        else:
            type_labels={t:type_aliases[t.__name__] for t in types}

        nx.draw_networkx_labels(
            G=self,
	    pos=pos,
	    ax=ax,
	    labels=type_labels,
            font_size=font_size
        )

        #plot computers
        nx.draw_networkx_nodes(
            G=self,
	    pos=pos,
	    ax=ax,
	    nodelist=computers,
	    node_color="lightblue"
        )
        def translate(c):
            return c.__wrapped__.__name__ if isinstance(c,_lru_cache_wrapper) else str(c)

        if computer_aliases is None:
            labels={c:translate(c) for c in computers}
        else:

            labels={c:computer_aliases[translate(c)] for c in computers}

        nx.draw_networkx_labels(
            G=self,
	    pos=pos,
	    ax=ax,
	    labels=labels,
            font_color='black',
            font_size=font_size
        )
        # draw edges
        nx.draw_networkx_edges(
            G=self,
            pos=pos,
            ax=ax
        )

        # draw target node
        if target_node is not None:
            nx.draw_networkx_nodes(
                G=self,
                pos=pos,
	        ax=ax,
	        nodelist=[target_node],
	        node_color="red",
                label="target"
            )
        ax.legend()
    

class DepGraph(nx.DiGraph):
    def root_node(self):
        return [n for n in  self.nodes if self.in_degree(n)==0][0]

    def __eq__(self, other):
        return (
            self.nodes == other.nodes and
            self.edges == other.edges
        )

    def __repr__(self):
        return (
            self.__class__.__name__ + "(\n"
            + reduce(
                lambda acc,el: acc + el,
                ["\n"+h.add_tab(h.add_tab("->" + el.__name__)) for el in self.nodes]
            )    
            + "\n)"
        )
    
    def draw_matplotlib(self,ax):
        gg=nx.DiGraph()
        gg.add_edges_from(
            map(
                lambda t: (t[0].__name__,t[1].__name__)
                ,self.edges()
            )
        )
        gg.add_nodes_from(
            map(
                lambda f: f.__name__
                ,self.nodes()
            )
        )
        nx.draw_networkx(gg,ax=ax,pos=nx.kamada_kawai_layout(gg))



    def required_mvars(
            self,
            given: Set[type]
        ):
        leaf_comps = [n for n in self.nodes if self.out_degree(n) == 0]
        args = reduce(
                lambda acc,comp: acc.union(h.input_mvars(comp)),
                leaf_comps,
                frozenset({})
        )
        return args if given is None else args.difference(given)
    
    def to_bipartite(self):
        cs=copy(self.nodes)
        B = BiGraph()
        # Add nodes with the node attribute "bipartite"
        B.add_nodes_from(
            [h.output_mvar(c) for c in cs],
            bipartite=0
        )

        B.add_nodes_from(
            cs,
            bipartite=1
        )
        # Add edges only between nodes of opposite node sets
        B.add_edges_from([ (c,h.output_mvar(c)) for c in cs])
        B.add_edges_from([ (a,c) for c in cs for a in h.input_mvars(c) ])
        return B


    def __hash__(self):
        return hash(
            (
                frozenset(self.nodes()),
                frozenset(self.edges())
            )
        )

    def jupyter_widget(
            self,
            computer_aliases=None,
            type_aliases=None,
            given=frozenset()
        ):
        cw1='20%'
        cw2='5%'
        cw3='50%'
        cw4=cw2
        cw5=cw1
        
        B=self.to_bipartite()

        with plt.ioff():
            fig = plt.figure(figsize=(6,5))
            #rect = 0, 0, 0.8, 1.2  # l, b, w, h
            rect = 0, 0, 1, 1  # l, b, w, h
            ax = fig.add_axes(rect)
        
        graph_out=Output(
            layout=Layout(
                height='auto',
                #width="{}%".format(thumbnail_width),
                width=cw3,
                #min_width=cw3,
                description="Bipartite Dependency Tree",
            )
        )
        with graph_out:
            ax.clear()
            #ax = fig.add_subplot(1, 1, 1)
            B.draw_matplotlib(
                ax,
                computer_aliases=computer_aliases,
                type_aliases=type_aliases,
                given=given
            )
            display(ax.figure)
            plt.close(fig)
        
        
        type_names_box=VBox(
            children=[
                Button(
                    layout= Layout(height='auto', min_width=cw1),
                    description=tn,
                    button_style='warning'
                )
                for tn in B.type_names()
            ]
        )
        computer_names_box=VBox(
            children=[
                Button(
                    layout= Layout(height='auto', min_width=cw5),
                    description=cn,
                    button_style='warning'
                )
                for cn in B.computer_names()
            ]
        )
        
        def type_aliases_box(type_aliases):
            return  [] if type_aliases is None else [VBox(
                children=[
                    Button(
                        layout= Layout(height='auto', min_width=cw2),
                        description=type_aliases[tn],
                        button_style='warning'
                    )
                    for tn in B.type_names()
                ]
            )]

        def computer_aliases_box(computer_aliases):
            return  [] if computer_aliases is None else [VBox(
                children=[
                    Button(
                        layout= Layout(height='auto', min_width=cw4),
                        description=computer_aliases[cn],
                        button_style='warning'
                    )
                    for cn in B.computer_names()
                ]
            )]

        line = Box(
            children=(
                [type_names_box] 
                + type_aliases_box(type_aliases) 
                + [graph_out]
                + computer_aliases_box(computer_aliases)
                + [computer_names_box]
            ),
            layout= Layout(
                overflow='scroll hidden',
                #border='3px solid black',
                #width='1000px',
                width='100%',
                height='',
                flex_flow='row',
                display='flex'
            )
        )
        return VBox(
            [
                #Label('Scroll horizontally:'),
                line
            ]
        )

    def compute_value(
        self,
        t: type,
        pvs: Set
    ):
        rg = copy(self).reverse()
        # compute the order of computations
        computations = nx.topological_sort(rg)
        
        # initialize the set of values to start from
        
        def apply(acc: Dict, comp: Callable) -> Dict:
            arg_classes = [
                p.annotation for p in signature(comp).parameters.values()
            ]
            arg_values = [acc[cl] for cl in arg_classes]
            res = copy(acc)
            res.update({h.output_mvar(comp): comp(*arg_values)})
            return res
        
        pv_dict = reduce(apply, computations, {type(v): v for v in pvs})
        
        return pv_dict[t]

def dep_graph(
        root_type: type,
        cs, #: Computerset,
        given: List[type] 
    ) -> DepGraph:
    
    # create a graph with the computers as nodes
    # so the nodes do not need to be added  as leafs (one step less)

    # find the computers that are not useful since they would compute variables alreday given  
    comps_given=tuple([c for c in cs if h.output_mvar(c) in given])
    
    comp_root = tuple([c for c in cs if h.output_mvar(c) == root_type])
    if len(comp_root) == 0:
        return DepGraph()
    else:
        css= cs.difference(given.union(comp_root,comps_given))
        g = sub_graph( comp_root, css)
        return g


@lru_cache
def sub_graph(
        comp_root: List[Callable],
        cs
    ) -> DepGraph:

    g=DepGraph()
    root_computer=comp_root[0]
    g.add_node(root_computer)
    
    params = tuple([ p.annotation for p in signature(root_computer).parameters.values()])

    def addsubgraph(g,param):
        gn=copy(g)
        cp = tuple([c for c in cs if h.output_mvar(c) == param])
        if len(cp)>0:
            param_computer = cp[0]
            gn.add_edge(root_computer, param_computer)
            css = cs.difference(cp) 
            sg = sub_graph(cp,css)
            gn.add_edges_from(sg.edges)
            gn.add_nodes_from(sg.nodes)
        return gn

    
    res = reduce(
            addsubgraph,
            params,
            g
    )
    return res
        


def computer_list_for_mvar(mvar, all_computers):
    return [ comp for comp in all_computers if h.output_mvar(comp) == mvar ] 


def computer_combies(cs,given):
    # dependency graphs in the sense of this module  only work if there
    # is only one possibility to compute a given variable.
    # If there is a variable with more than one computer yielding it,
    # we get alternative dep graphs.
    # We can compute a variable if one of the dep graphs is computable 
    # with the given values.
    # This function finds all the given  unique computersets.

    
    comp_lists = [computer_list_for_mvar(var,cs) for  var in h.all_output_types(cs).difference(given)]
    return h.list_mult(comp_lists)
    
def all_dep_graphs(root_type,cs,given):
    return map(
            lambda combi:dep_graph(root_type,frozenset(combi),given),
            computer_combies(cs,given)
    )


def computable_dep_graphs(root_type,cs,given):
    res = filter(
        lambda g: g.required_mvars(given).issubset(given),
        all_dep_graphs(root_type,cs,given)
    )
    #from IPython import embed; embed()
    return res


def shortest_computable_dep_graph(root_type, cs, given):
    cgs = tuple(computable_dep_graphs(root_type, cs, given))
    if len(cgs) > 0:
        return sorted(
            computable_dep_graphs(
                root_type,
                cs,
                given
            ),
            key=lambda g: len(g.edges)
        )[0]
    else:
        raise Exception("This variable can not computed from the given values")


def computer_dict(cs):
    return {var: computer_list_for_mvar(var,cs) for  var in h.all_output_types(cs)}


def duplicated_computer_dict(cs):
    cd=computer_dict(cs)
    return { k:v for k,v in cd.items() if len(v)>1}
