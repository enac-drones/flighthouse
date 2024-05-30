import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from ...utils.json_utils import load_from_json

def visualise3D(filename:str, history_length:int = 50, show_sheets:bool = True, interval:float = 1):
    '''3D plot to visualise drone paths with trail'''
    print(filename)
    output_data = load_from_json(filename)
    vehicles = output_data['vehicles']
    paths = [v['path'] for v in vehicles]
    paths = [np.array(path).tolist() for path in paths]

    buildings = output_data.get('buildings', [])


    # Initialize drones
    N = len(paths)  # Number of drones
    drones = np.full((N, 3), np.nan)  # Initial positions of the drones
    paths_history = [np.full((history_length, 3), np.nan) for _ in range(N)]  # History of positions for each drone

    # Set up the figure and 3D axis
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([0, 10])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    fig.set_size_inches(8, 8)

    # Initial plot for drones
    plot, = ax.plot([], [], [], linestyle=' ', marker='o', color='b')

    # Initial plot for paths
    colours = ['r', 'b', 'g', 'k', 'c']
    path_plots = [ax.plot([], [], [], f'{colours[_ % len(colours)]}-')[0] for _ in range(N)]

    if show_sheets:
        # Initialize one Poly3DCollection per drone for the surface
        surface_collections = [Poly3DCollection([], alpha=0.25) for _ in range(N)]
        for idx, poly in enumerate(surface_collections):
            poly.set_facecolor(colours[idx % len(colours)])
            ax.add_collection3d(poly)

    # Initialize an external structure to manage vertices for each drone
    drone_path_vertices = [[] for _ in range(N)]

    def update_paths(paths_history):
        for idx, history in enumerate(paths_history):
            # Update path plot
            path_plots[idx].set_data(history[:, 0], history[:, 1])
            path_plots[idx].set_3d_properties(history[:, 2])


    def update_stemlines(paths_history):
        for idx, history in enumerate(paths_history):
            #update the sheets
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
        nonlocal i, drones_stopped
        for idx, path in enumerate(paths):
            if i < len(path):
                current_position = path[i]
            else:
                current_position = path[-1]
                drones_stopped[idx] = True
            drones[idx, :3] = current_position
            # Update history
            paths_history[idx] = np.roll(paths_history[idx], -1, axis=0)
            paths_history[idx][-1, :] = current_position

        if all(drones_stopped):
            i = 0
            drones_stopped = [False] * N
            for idx in range(N):
                paths_history[idx][:] = np.nan
                drone_path_vertices[idx] = []

        i += 1
        return drones

    # Function to update the plot
    def update_plot(frame, plot, drones, paths_history):
        drones = update_positions(drones, paths_history)
        plot.set_data(drones[:, 0], drones[:, 1])
        plot.set_3d_properties(drones[:, 2])
        update_paths(paths_history)
        if show_sheets:
            update_stemlines(paths_history)

        return plot,

    # Function to add buildings to the plot
    def add_buildings(buildings):
        for building in buildings:
            vertices = np.array(building['vertices'])
            base = vertices[:, :2].tolist()
            height = vertices[0, 2]
            base.append(base[0])  # Close the polygon

            for i in range(len(base) - 1):
                x = [base[i][0], base[i+1][0], base[i+1][0], base[i][0]]
                y = [base[i][1], base[i+1][1], base[i+1][1], base[i][1]]
                z = [0, 0, height, height]
                verts = [list(zip(x, y, z))]
                poly = Poly3DCollection(verts, alpha=0.7, edgecolor='k')
                poly.set_facecolor('gray')
                ax.add_collection3d(poly)

    # Add buildings to the plot
    add_buildings(buildings)

    i = 0
    drones_stopped = [False] * N

    # Creating animation
    ani = FuncAnimation(fig, update_plot, fargs=(plot, drones, paths_history), frames=None, interval=interval, blit=False, cache_frame_data=False)
    plt.show()

# Example usage:
# plot_drone_paths('path/to/your/input_data.json')
