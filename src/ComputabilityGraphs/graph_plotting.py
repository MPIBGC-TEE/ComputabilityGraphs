from pygraphviz.agraph import AGraph
from typing import Callable
from functools import reduce
from frozendict import frozendict
from bokeh.plotting import figure
from bokeh.models import (
    BoxSelectTool,
    HoverTool,
    TapTool,
    ColumnDataSource,
    LabelSet,
#)
#from bokeh.models import (
    Ellipse,
    GraphRenderer,
    StaticLayoutProvider,
    BoxSelectTool,
    Circle,
    EdgesAndLinkedNodes,
    EdgesOnly,
    NodesOnly,
    HoverTool,
    MultiLine,
    NodesAndLinkedEdges,
    Plot,
    Range1d,
    TapTool,
    ColumnDataSource,
    Label,
    LabelSet,
    Range1d
)
from bokeh.palettes import Spectral4,Cividis256
from bokeh.palettes import Spectral4,Cividis256
from functools import reduce
from typing import List,Tuple
import networkx as nx
import numpy as np

import ComputabilityGraphs.graph_helpers as gh
import ComputabilityGraphs.fast_graph_helpers as fgh
from .helpers import (
    merge_dicts,
)
from .str_helpers import (
    pretty_name,
    node_2_string,
    nodes_2_string,
    varset_2_string,
    varsettuple_2_string,
    compset_2_string
)
from .ComputerSet import ComputerSet
from .ComputerSetSet import ComputerSetSet
from . import bokeh_helpers as bh 


def draw_sequence(fig, tups):
    axs = fig.subplots(len(tups), 1, sharex=True, sharey=True)
    for i, tup in enumerate(tups):
        g, title = tup
        axs[i].set(frame_on=True)
        # nx.draw(g,ax=axs[i],frame_on=True)
        draw_ComputerSetMultiDiGraph_matplotlib(axs[i], g)
        axs[i].set(title=title)


def draw_update_sequence(
    computers,
    max_it,
    fig,
    mvar_aliases=frozendict({}),
    computer_aliases=frozendict({})
):
    lg = [g for g in gh.update_generator(computers, max_it=max_it)]
    nr = len(lg)
    fig.set_size_inches(20, 20 * nr)
    pos = nx.spring_layout(lg[-1])
    # layout alternatives
    # pos = nx.spring_layout(lg[-1], iterations=20)
    # pos = nx.circular_layout(lg[-1] )
    # pos = nx.kamada_kawai_layout (lg[-1])
    # pos = nx.planar_layout (lg[-1])
    # pos = nx.random_layout (lg[-1])
    # pos = nx.shell_layout (lg[-1])
    # pos = nx.spectral_layout (lg[-1])
    # pos = nx.spiral_layout (lg[-1])
    axs = fig.subplots(nr, 1, sharex=True, sharey=True)
    for i in range(nr):
        draw_ComputerSetMultiDiGraph_matplotlib(
            axs[i], lg[i], mvar_aliases, computer_aliases, pos=pos
        )


#def draw_FastGraph_matplotlib(
#    ax,
#    spsg,
#    mvar_aliases=frozendict({}),
#    computer_aliases=frozendict({}),
#    targetNode=None,
#    pos=None,
#    **kwargs
#):
#    top_nodes = frozenset({n for n, d in spsg.nodes(data=True) if d["bipartite"] == 0})
#    bottom_nodes = frozenset( set(spsg) - top_nodes )
#    set_labels = {n: varset_2_string(n, mvar_aliases) for n in top_nodes}
#    decomp_labels = {n: varsettuple_2_string(n, mvar_aliases) for n in bottom_nodes}
#    labels = merge_dicts(set_labels, decomp_labels)
#    if pos is None:
#        # layout alternatives
#        pos = nx.spring_layout(spsg)
#        # pos = nx.circular_layout(spsg)
#        # pos = nx.spring_layout(spsg, iterations=20)
#        # pos = nx.circular_layout(spsg )
#        ##pos = nx.kamada_kawai_layout(spsg) #funny artefacts
#        # pos = nx.planar_layout(spsg)
#        # pos = nx.random_layout(spsg)
#        # pos = nx.shell_layout(spsg)
#        # pos = nx.spectral_layout(spsg)
#        # pos = nx.spiral_layout(spsg)
#    
#    nx.draw_networkx_labels(
#        spsg,
#        labels=labels,
#        ax=ax,
#        font_color='black',
#        pos=pos,
#        **kwargs
#    )
#    nx.draw_networkx_edges(
#        spsg,
#        #labels=labels,
#        ax=ax,
#        pos=pos,
#    )
#    nx.draw_networkx_nodes(
#        spsg,
#        ax=ax,
#        pos=pos,
#        node_size=1000,
#        nodelist=list(top_nodes),
#        node_color='orange',
#        alpha=0.8
#    )
#    nx.draw_networkx_nodes(
#        spsg,
#        ax=ax,
#        pos=pos,
#        nodelist=list(bottom_nodes),
#        node_color='g',
#        alpha=0.8
#    )
#    if targetNode is not None:
#        res = gh.minimal_startnodes_for_node(spsg, targetNode)
#        nx.draw_networkx_nodes(
#            spsg,
#            pos,
#            nodelist=[targetNode],
#            node_color='r',
#            alpha=0.8
#        )
#        nx.draw_networkx_nodes(
#            spsg,
#            pos,
#            nodelist=list(res),
#            node_color='r',
#            alpha=0.4
#        )
#
#    ax.axis("On")
#
#    # at the moment it is not possible to draw
#    # more than one edge (egde_lables) between nodes
#    # directly (no edgelabels for MultiDiGraphs)
#    # therefore we draw only one line for all computersets
#    def edgeDict_to_string(ed):
#        target = "computer_sets"
#        if target in ed.keys():
#            comp_sets=ed[target]
#            comp_set_strings= [compset_2_string(cs, computer_aliases) for cs in comp_sets]
#            res = "\n".join(comp_set_strings)
#        else:
#            res=''
#        return res 
#
#    edge_labels = {e: edgeDict_to_string(spsg.get_edge_data(*e)) for e in spsg.edges()}
#
#    nx.draw_networkx_edge_labels(spsg, ax=ax, edge_labels=edge_labels, pos=pos)
#    mvar_aliases_inv = {val: key for key, val in mvar_aliases.items()}
#    for i, k in enumerate(sorted(mvar_aliases_inv.keys())):
#        ax.text(0, 0 - i / len(mvar_aliases), k + ": " + mvar_aliases_inv[k])


def draw_ComputerSetDiGraph_matplotlib(
    spsg: nx.DiGraph,
    ax,
    pos=None,
    **kwargs
):
    if pos is None:
        pos = nx.spring_layout(spsg)
        # pos = nx.circular_layout(spsg)

    nx.draw(
        spsg,
        labels={n: node_2_string(n) for n in spsg.nodes()},
        ax=ax,
        node_size=2000,
        node_shape="s",
        pos=pos,
        **kwargs
    )
    for e in spsg.edges():
        print(spsg.get_edge_data(*e))

    edge_labels = {
        e: compset_2_string(spsg.get_edge_data(*e)["computers"]) for e in spsg.edges()
    }
    nx.draw_networkx_edge_labels(spsg, ax=ax, edge_labels=edge_labels, pos=pos)

def draw_ComputerSetMultiDiGraph_matplotlib(
    ax,
    spsg,
    mvar_aliases=frozendict({}),
    computer_aliases=frozendict({}),
    targetNode=None,
    pos=None,
    **kwargs
):
    if pos is None:
        # layout alternatives
        # pos = nx.spring_layout(spsg)
        # pos = nx.circular_layout(spsg)
        # pos = nx.spring_layout(spsg, iterations=20)
        # pos = nx.circular_layout(spsg )
        pos = nx.kamada_kawai_layout(spsg)
        # pos = nx.planar_layout(spsg)
        # pos = nx.random_layout(spsg)
        # pos = nx.shell_layout(spsg)
        # pos = nx.spectral_layout(spsg)
        # pos = nx.spiral_layout(spsg)
    nx.draw(
        spsg,
        labels={n: node_2_string(n, mvar_aliases) for n in spsg.nodes()},
        ax=ax,
        node_size=1000,
        # node_shape='s',
        pos=pos,
        **kwargs
    )
    if targetNode is not None:
        res = gh.minimal_startnodes_for_node(spsg, targetNode)
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
    # and assemble the label from the different edges
    def edgeDict_to_string(ed):
        target = "computers"
        comp_sets = [v[target] for v in ed.values() if target in v.keys()]
        comp_set_strings = [compset_2_string(cs, computer_aliases) for cs in comp_sets]
        res = "\n".join(comp_set_strings)
        # print(res)
        return res

    edge_labels = {e: edgeDict_to_string(spsg.get_edge_data(*e)) for e in spsg.edges()}

    nx.draw_networkx_edge_labels(spsg, ax=ax, edge_labels=edge_labels, pos=pos)
    mvar_aliases_inv = {val: key for key, val in mvar_aliases.items()}
    for i, k in enumerate(sorted(mvar_aliases_inv.keys())):
        ax.text(0, 0 - i / len(mvar_aliases), k + ": " + mvar_aliases_inv[k])




def bokeh_plot(
        G: nx.MultiDiGraph,
        targetNode=None
    ):
    
    # G is a MultiDiGraph ( n directed edges between 2 nodes)
    # Edges are represented as triplets (sourc,target,ind) for ind in range(n))
    e_tuples=set([(s,t) for s,t,ind in G.edges])
    # We will first transform it into a DiGraph 
    g=nx.DiGraph()
    for e in e_tuples:
        src,target=e
        # G.get_edge_data(s,t) yields a dict of lenght n  of tuples of (ind, edgedata)
        # we get rid of the ind part and create a set of computersets
        t=G.get_edge_data(src,target)
        #from IPython import embed;embed()
        css=ComputerSetSet([ComputerSet(d['computers'])  for ind,d in t.items()])
        g.add_edge(src,target,computerSetSet=css)


        

    gs=nx.DiGraph()
    # having projected the MultiDigraph G to the DiGraph g
    # we stringify g by converting all attr to string and all
    for n in g.nodes:
        gs.add_node(node_2_string(n))


    attr_key='computerSetSet'
    for e in g.edges:
        src, target = e
        css = g.get_edge_data(src, target)[attr_key] #this is a tupel (one element per edge between 
        new_edge=(
            node_2_string(src), 
            node_2_string(target)
        )
        gs.add_edge(
            *new_edge
        )
        gs.get_edge_data(*new_edge).update({attr_key:str(css)})

    plot = figure(
            title="Computability Graphs",
            #plot_width=1700,
            #plot_height=550
    )
    plot.sizing_mode="scale_width"
    #node_hover_tool = HoverTool(tooltips=[("index", "$index"), ("start","@start"),("end","@end"),("test","@test")])
    node_hover_tool = HoverTool(tooltips=[("start","@start"),("end","@end"),(attr_key, "@"+attr_key)])
    plot.add_tools(node_hover_tool, TapTool(), BoxSelectTool())
    layout=nx.spring_layout
    Graph_Layout = layout(G)
    #graph_layout = layout(gs)
    graph_layout = {node_2_string(k):v for k,v in Graph_Layout.items()}
    names= list(graph_layout.keys())
    #names= [str(k) for k in graph_layout.keys()]
    source = ColumnDataSource(
            data=dict(
                xs=[graph_layout[n][0] for n in names],
                ys=[graph_layout[n][1] for n in names],
                names=names 
            )
    )
    labels = LabelSet(
            x='xs', 
            y='ys', 
            text='names',
            x_offset=-15, 
            y_offset=-15, 
            source=source, 
            border_line_color='black',
            background_fill_color='white',
            #render_mode='canvas' #caused testerror
    )

    node_dict = dict()
    node_dict['index'] = list(gs.nodes())
    N=gs.number_of_nodes()
    node_dict['color'] = Cividis256[:N]
    n_steps=100

    steps = [i/float(n_steps) for i in range(n_steps)]

    graph_renderer = GraphRenderer()

    node_keys = graph_renderer.node_renderer.data_source.data['index']

    # Convert edge attributes
    edge_dict = dict()

    attr_key='computerSetSet'
    values = [edge_attr[attr_key] if attr_key in edge_attr.keys() else None
              for _, _, edge_attr in gs.edges(data=True)]

    edge_dict[attr_key] = values

    edge_dict['start'] = [x[0] for x in gs.edges()]
    edge_dict['end'] = [x[1] for x in gs.edges()]
    edge_dict['test'] = values
    
    xs_ys=[ 
        #bh.double_bezier(
        #    start_point=graph_layout[sp],
        #    end_point=graph_layout[ep],
        #    #control_vector=(1,1),
        #    control_vector=(1e-4,1e-4),
        #    steps=steps
        #)
        bh.double_straight(
            start_point=graph_layout[sp],
            end_point=graph_layout[ep],
            steps=steps
        )
        for (sp,ep) in gs.edges()
    ]    
    edge_dict['xs'] = [x for x,y in xs_ys]
    edge_dict['ys'] = [y for x,y in xs_ys]


    graph_renderer.node_renderer.data_source.data = node_dict
    graph_renderer.edge_renderer.data_source.data = edge_dict

    graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    #graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.glyph = Circle(size=10, fill_color='color')
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=25, fill_color=Spectral4[1])
    
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)
    
    graph_renderer.inspection_policy = EdgesAndLinkedNodes()
    #graph_renderer.selection_policy = NodesAndLinkedEdges()
    #graph_renderer.inspection_policy = EdgesOnly()
    #graph_renderer.inspection_policy = NodesOnly()
    #graph_renderer.inspection_policy = NodesAndLinkedEdges()
    
    
    print(type(list(Graph_Layout.keys())[0]))
    if targetNode is not None:
        #res = gh.minimal_startnodes_for_node(G, targetNode)
        x,y=Graph_Layout[targetNode]
        plot.circle(
                x,
                y,
                size=15, 
                fill_color='red'
        )
    plot.renderers.append(graph_renderer)
    #plot.add_layout(labels)
    return plot


def AGraphComputerSetMultiDiGraph(spsg: nx.MultiDiGraph, cf: Callable) -> AGraph:
    A = nx.nx_agraph.to_agraph(spsg)
    A = AGraph(directed=True)
    A.node_attr["style"] = "filled"
    A.node_attr["shape"] = "rectangle"
    A.node_attr["fixedsize"] = "false"
    A.node_attr["fontcolor"] = "black"

    for node in spsg.nodes:
        A.add_node(node_2_string(node))
    edges = spsg.edges(data=True)
    for edge in edges:
        s, t, data_dict = edge
        computer_set = data_dict["computers"]
        ss, st = tuple(map(node_2_string, (s, t)))
        A.add_edge(ss, st)
        Ae = A.get_edge(ss, st)
        Ae.attr["label"] = "\n".join([c.__name__ for c in computer_set])
    return A


def AGraphComputerMultiDiGraph(spsg: nx.MultiDiGraph, cf: Callable) -> AGraph:
    A = nx.nx_agraph.to_agraph(spsg)
    A = AGraph(directed=True)
    A.node_attr["style"] = "filled"
    A.node_attr["shape"] = "rectangle"
    A.node_attr["fixedsize"] = "false"
    A.node_attr["fontcolor"] = "black"

    for node in spsg.nodes:
        A.add_node(node_2_string(node))
    edges = spsg.edges(data=True)
    for edge in edges:
        s, t, data_dict = edge
        computer_set = data_dict["computers"]
        for c in computer_set:
            ss, st = tuple(map(node_2_string, (s, t)))
            A.add_edge(ss, st)
            Ae = A.get_edge(ss, st)
            Ae.attr["color"] = cf(c)
            Ae.attr["fontcolor"] = cf(c)
            Ae.attr["label"] = c.__name__

    return A
