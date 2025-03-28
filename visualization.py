"""Visualization"""
import networkx as nx
import plotly
from graph import Graph


def visualize_graph_plotly(g: Graph, n: int) -> None:
    """Generate a visualization for g using n arbitrary vertices.
    If g has less than n vertices, plot all vertices."""

    vis = nx.DiGraph()
    word_vertices = [y for y in g.vertices.values() if isinstance(y.word, str)]
    added_vertices = []

    # Make network
    for v in word_vertices:
        if len(added_vertices) == n:
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
    annotations = []
    for u, v in vis.edges():
        zero_coordinates = pos[u]
        one_coordinates = pos[v]
        edge_x.extend([zero_coordinates[0], one_coordinates[0], None])
        edge_y.extend([zero_coordinates[1], one_coordinates[1], None])

        # Add arrow annotation
        annotations.append({"ax": zero_coordinates[0], "ay": zero_coordinates[1], "x": one_coordinates[0],
                            "y": one_coordinates[1], "xref": "x", "yref": "y", "axref": "x", "ayref": "y",
                            "showarrow": True, "arrowhead": 3, "arrowsize": 1.5, "arrowwidth": 1.5,
                            "arrowcolor": "gray"})

    # Create figure
    figure = plotly.graph_objs.Figure()

    # Add edges to figure
    figure.add_trace(plotly.graph_objs.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line={"width": 1, "color": 'gray', 'shape': 'linear'},
        hoverinfo='none',
    ))

    # Add nodes to figure
    nodes = [pos[node][0] for node in vis.nodes()], [pos[node][1] for node in vis.nodes()]

    figure.add_trace(plotly.graph_objs.Scatter(
        x=nodes[0], y=nodes[1],
        mode='markers+text',
        text=list(vis.nodes()),
        textposition="top center",
        hoverinfo='text',
        marker={"size": 10, "color": 'blue', "opacity": 0.8}
    ))

    # Specify layout with arrows
    figure.update_layout(
        showlegend=False,
        title=f"Word Map for {g.file_name}",
        title_x=0.5,
        title_y=0.95,
        hovermode='closest',
        plot_bgcolor='white',
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        annotations=annotations
    )

    # Display
    figure.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['graph, networkx, plotly'],
        'max-line-length': 120
    })
