"""Visualization"""

from graph import Graph
import networkx as nx
import plotly


def visualize_graph_plotly(g: Graph, n: int):
    """Generate a visualization for g using n arbitrary vertices.
    If g has less than n vertices, plot all vertices."""

    vis = nx.DiGraph()
    word_vertices = [v for v in g.vertices.values() if isinstance(v.word, str)]
    max_vertices = n
    added_vertices = []

    # Make network
    for v in word_vertices:
        if len(added_vertices) == max_vertices:
            break
        else:
            vis.add_node(v.word)
            added_vertices.append(v)
    for v in added_vertices:
        for u in v.neighbours:
            if u in added_vertices:
                vis.add_edge(v.word, u.word, weight=v.neighbours[u])
    pos = nx.spring_layout(vis, weight="weight", seed=42, iterations=50)

    # Extract coordinates
    edge_x = []
    edge_y = []
    for u, v in vis.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Create figure
    figure = plotly.graph_objs.Figure()

    # Add edges to figure
    figure.add_trace(plotly.graph_objs.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='gray', shape='linear'),
        hoverinfo='none',
    ))

    # Add nodes to figure
    node_x = [pos[node][0] for node in vis.nodes()]
    node_y = [pos[node][1] for node in vis.nodes()]
    figure.add_trace(plotly.graph_objs.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=list(vis.nodes()),
        marker=dict(
            size=10,
            color='blue',
            opacity=0.8
        )
    ))

    # Specify layout
    figure.update_layout(
        showlegend=False,
        title=f"Word Map for {g.file_name}",
        title_x=0.5,
        title_y=0.95,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Display
    figure.show()
