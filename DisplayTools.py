import numpy as np
from plotly import graph_objs as go

def display_solution_path(path, state_space_dim = 3):
    processed_path = np.fromstring(path.printAsMatrix(), dtype=float, sep=' ')
    processed_path = processed_path.reshape(-1, state_space_dim)

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=processed_path[:, 0],
        y=processed_path[:, 1],
        z=processed_path[:, 2],
        mode='lines+markers',
        marker=dict(size=4),
        line=dict(width=2)
    ))

    fig.show()