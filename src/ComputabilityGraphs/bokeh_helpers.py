import numpy as np
import inspect
from bokeh.io import output_file, show
from bokeh.plotting import figure#, from_networkx
from bokeh.models import (
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
from functools import reduce
from typing import List,Tuple
from .str_helpers import (
    pretty_name,
    node_2_string,
    nodes_2_string,
    varset_2_string,
    varsettuple_2_string,
    compset_2_string
)
def veclist_to_coordlists(veclist):
    xs=[v[0] for v in veclist]
    ys=[v[1] for v in veclist]
    return xs,ys
    #return list(zip(*veclist))

def norm(vec):
    return np.sqrt(np.dot(vec,vec))

def with_arrow_head(
        xs: List[float],
        ys: List[float], 
        width: float = 0.5,
        length: float =0.5,
    )->Tuple[List[float],List[float]]:
    
    last_point=np.array([
        xs[-1],
        ys[-1]
    ])
    second_last_point=np.array([
        xs[-2],
        ys[-2]
    ])
    last_vector=last_point-second_last_point
    last_vector_n=last_vector/norm(last_vector)
    #print('last_vector',last_vector)
    left_head_vector=np.array([
        -last_vector_n[1],
         last_vector_n[0]
    ])    
    #print('left_head_vector',left_head_vector)
    right_head_vector = -left_head_vector
    left_head_point=last_point -length*last_vector_n +width*left_head_vector
    
    right_head_point = last_point - length*last_vector_n  +  width*right_head_vector
    #we go first from the tip to left head
    left_stroke=[left_head_point,last_point]
    right_stroke=[right_head_point,last_point]

    
    left_xs,left_ys = veclist_to_coordlists(left_stroke)
    right_xs,right_ys = veclist_to_coordlists(right_stroke)
    xss=xs+left_xs+right_xs
    yss=ys+left_ys+right_ys
    return xss,yss

def bezier(start, end, control, steps):
    return [(1-s)**2*start + 2*(1-s)*s*control + s**2*end for s in steps]

def straight(start, end, steps):
    delta=end-start
    return [start + s*delta  for s in steps]

def double_bezier(
        start_point,
        end_point,
        control_vector,
        steps
    ):
    start_x,start_y = start_point
    end_x,end_y = end_point
    control_x,control_y = control_vector
    xs = bezier(start_x,end_x,control_x,steps)
    ys = bezier(start_y,end_y,control_y,steps)
    xss,yss=with_arrow_head(xs,ys,0.01,0.01)
    return (
        xss,
        yss
    )

def double_straight(
        start_point,
        end_point,
        steps
    ):
    start_x,start_y = start_point
    end_x,end_y = end_point
    xs = straight(start_x,end_x,steps)
    ys = straight(start_y,end_y,steps)
    xss,yss=with_arrow_head(xs,ys,0.02,0.03)
    return (
        xss,
        yss
    )

def _handle_sublists(values):
    # if any of the items is non-scalar, they all must be
    if any(isinstance(x, (list, tuple)) for x in values):
        if not all(isinstance(x, (list, tuple)) for x in values if x is not None):
            raise ValueError("Can't mix scalar and non-scalar values for graph attributes")
        return [[] if x is None else list(x) for x in values]
    return values


