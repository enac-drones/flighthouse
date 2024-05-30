import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import threading
import time
from gflow.utils.json_utils import load_from_json

def simulation_visualize3Dtrails(filename, history_length:int = 50):
    '''3D plot to visualise drone paths with trail'''
    output_data = load_from_json(filename)
    vehicles = output_data['vehicles']
    paths = [v['path'] for v in vehicles]
    paths = [(np.array(path) + np.array([0, 0, 4])).tolist() for path in paths]

    # Initialize drones
    N = len(paths)  # Number of drones
    drones = np.full((N, 3), np.nan)  # Initial positions of the drones
    paths_history = [np.full((history_length, 3), np.nan) for _ in range(N)]  # History of positions for each drone

    # Set up the figure and 3D axis
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([0, 10])

    # Hide all grids and axes
    ax.grid(False)            # Turn off the grid
    ax.set_xticks([])         # Remove x-axis ticks
    ax.set_yticks([])         # Remove y-axis ticks
    ax.set_zticks([])         # Remove y-axis ticks

    fig.set_size_inches(8, 8)

    # Initial plot for drones
    plot, = ax.plot([], [], [], linestyle=' ', marker='o', color='b')

    # Initial plot for paths
    colours = ['r', 'b', 'g', 'k', 'c']
    path_plots = [ax.plot([], [], [], f'{colours[_ % len(colours)]}-')[0] for _ in range(N)]

    # Initialize one Poly3DCollection per drone for the surface
    surface_collections = [Poly3DCollection([], alpha=0.25) for _ in range(N)]
    for idx, poly in enumerate(surface_collections):
        poly.set_facecolor(colours[idx % len(colours)])
        ax.add_collection3d(poly)

    # Assuming initialization of paths_history and surface_collections is done

    # Initialize an external structure to manage vertices for each drone
    # This will hold the current vertices for the visible segments of the path
    drone_path_vertices = [[] for _ in range(N)]

    def update_stemlines_and_paths(paths_history):
        for idx, history in enumerate(paths_history):
            # Update path plot
            path_plots[idx].set_data(history[:, 0], history[:, 1])
            path_plots[idx].set_3d_properties(history[:, 2])

            if np.count_nonzero(~np.isnan(history[:, 0])) > 1:
                # Get the index of the last valid point
                valid_indices = np.where(~np.isnan(history[:, 0]))[0]
                if len(valid_indices) > 1:
                    new_point_idx = valid_indices[-1]
                    prev_point_idx = valid_indices[-2]

                    # Create vertices for the new segment
                    new_segment_verts = [
                        [history[prev_point_idx, :2].tolist() + [0],
                         history[new_point_idx, :2].tolist() + [0],
                         history[new_point_idx, :].tolist(),
                         history[prev_point_idx, :].tolist()]]

                    # Update the vertices list for this drone
                    # If the list is at max capacity, remove the oldest segment
                    if len(drone_path_vertices[idx]) >= history_length:
                        drone_path_vertices[idx].pop(0)
                    drone_path_vertices[idx].append(new_segment_verts[0])

                    # Update the Poly3DCollection with the new set of vertices
                    surface_collections[idx].set_verts(drone_path_vertices[idx])

    def update_positions(drones, paths_history):
        nonlocal i
        for idx, path in enumerate(paths):
            current_position = path[i % len(path)]
            drones[idx, :3] = current_position
            # Update history
            paths_history[idx] = np.roll(paths_history[idx], -1, axis=0)
            paths_history[idx][-1, :] = current_position
        i += 1
        return drones

    # Function to update the plot
    def update_plot(frame, plot, drones, paths_history):
        drones = update_positions(drones, paths_history)
        plot.set_data(drones[:, 0], drones[:, 1])
        plot.set_3d_properties(drones[:, 2])
        update_stemlines_and_paths(paths_history)
        return plot,

    i = 1
    # Creating animation
    ani = FuncAnimation(fig, update_plot, fargs=(plot, drones, paths_history), frames=None, interval=1, blit=False, cache_frame_data=False)
    plt.show()


