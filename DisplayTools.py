import numpy as np
from plotly import graph_objects as go
import networkx as nx
import io

def display_solution_path_SE2(path):
    state_space_dim = 3
    processed_path = np.fromstring(path.printAsMatrix(), dtype=float, sep=' ')
    processed_path = processed_path.reshape(-1, state_space_dim)

    num_points = processed_path.shape[0]
    colors = ['green'] + ['blue'] * (num_points - 2) + ['red']  # First point green, last point red, others blue


    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=processed_path[:, 0],
        y=processed_path[:, 1],
        z=processed_path[:, 2],
        mode='lines+markers',
        marker=dict(size=4, color=colors),
        line=dict(width=2)
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Theta"
        ),
        title="Path in SE2 state space"
    )

    fig.show()

def convert_to_printable_graph(planner_graph):
    """
    This is a simple implementation of graphML parsing, there are probably better ways to do that
    """

    graph_elemets = planner_graph.split('\n')

    nodes = {}
    fill_el = False    # Assuming right after node name comes node coordinates element
    for el in graph_elemets:
        if fill_el:
            coords_str = el.split('>')[1].split('<')[0]
            nodes[node_name] = np.fromstring(coords_str, dtype=float, sep=',')
            fill_el = False


        if "node id" in el:
            node_name = el.split('\"')[1]
            fill_el = True


    edges = {}
    for el in graph_elemets:
        if "edge id" in el:
            splitted_el = el.split('\"')
            edge_name = splitted_el[1]
            source = splitted_el[3]
            dest = splitted_el[5]
            edges[edge_name] = (source, dest)

    return nodes, edges

def display_roadmap_graph(planer_data):
    G_V, G_E = convert_to_printable_graph(planer_data.printGraphML())

    # Extract edges geometry
    edge_x, edge_y, edge_t = [], [], []
    for edge in G_E.values():
        x0, y0, t0 = G_V[edge[0]]
        x1, y1, t1 = G_V[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_t.extend([t0, t1, None])

    node_x, node_y, node_t = list(zip(*list(G_V.values())))

    fig = go.Figure()

    # Create Plotly traces
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_t,
        line=dict(width=1, color='black'),
        hoverinfo='none',
        mode='lines'
    ))

    num_points = len(node_x)
    start_ind, goal_ind = planer_data.getStartIndex(0), planer_data.getGoalIndex(0)
    colors = ['blue'] * num_points
    colors[start_ind] = 'green'
    colors[goal_ind] = 'red'

    fig.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=node_t,
        mode='markers+text',
        text=[node for node in G_V.keys()],
        marker=dict(size=10, color=colors),
        hoverinfo='text'
    ))

    # Plot
    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Theta"
        ),
        title="Path in SE2 state space"
    )

    fig.show()