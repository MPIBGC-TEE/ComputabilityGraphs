from frozendict import frozendict
def pretty_name(mvar: type, aliases: frozendict = frozendict({})) -> str:
    if len(aliases) == 0:
        s = mvar.__name__
        # return ((s.split('<')[1]).split('>')[0]).split('.')[-1]
    else:
        s = aliases[mvar.__name__]
    return s

def node_2_string(node, aliases=frozendict({})):
    return "{" + ",".join([pretty_name(v, aliases) for v in node]) + "}"

def varset_2_string(node, aliases=frozendict({})):
    return "{" + ",".join([pretty_name(v, aliases) for v in node]) + "}"

def varsettuple_2_string(node_tuple, aliases=frozendict({})):
    active,passive = node_tuple 
    res = "{" + ",".join([pretty_name(v, aliases) for v in active]) + "}" \
            + "{" + ",".join([pretty_name(v, aliases) for v in passive]) + "}"
    return res    

def nodes_2_string(nodes, aliases=frozendict({})):
    return "[ " + ",".join([node_2_string(n, aliases) for n in nodes]) + " ]"

def decompositions_2_string(
        decompositions, 
        aliases=frozendict({})
    ):
    return "{ " + ",".join(
        [varsettuple_2_string(d) for d in decompositions]
    ) + "}"

def compset_2_string(compset, aliases=frozendict({})):
    return "{" + ",".join([pretty_name(c, aliases) for c in compset]) + "}"


def edge_2_string(e):
    return "(" + node_2_string(e[0]) + "," + node_2_string(e[1]) + ")"

