"""Visualization"""

from graphviz import Digraph
from graph import Graph

def load_graph(g: Graph):
    dot = Digraph('word map')
    for v in g.vertices:
        dot.node(v.item)
    for v in g.vertices:
        for u in v.neighbors:
            dot.edge(v.item, u.item)
