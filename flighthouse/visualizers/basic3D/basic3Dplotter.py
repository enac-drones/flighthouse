import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ...utils.json_utils import load_from_json
import time
import threading

def simulation_visualize3D(filename):
    output_data = load_from_json(filename)
    vehicles = output_data['vehicles']
    paths = [v['path'] for v in vehicles]

    # Initialize drones
    N = len(paths)  # Number of drones
    drones = np.full((N, 3), np.nan)  # Initial positions of the drones

    # Set up the figure and 3D axis
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    x, y, z = drones[:, 0], drones[:, 1], drones[:, 2]
    markerline, stemlines, baseline = ax.stem(x, y, z, linefmt='--', markerfmt='ob', basefmt=' ')

    # Initial plot
    plot, = ax.plot(x, y, z, linestyle=' ', marker='o', color='b')

    # Setting the plot limits
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([0, 10])
    # Set the axes labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # Set the size of the plot to be large
    fig.set_size_inches(8, 8)

    def update_positions(drones):
        nonlocal i
        for idx, path in enumerate(paths):
            drones[idx, :3] = path[:i][-1]
            drones[idx, 2] = 4
        i += 1
        i = max(i % len(paths[0]), 1)  # Loop back to the beginning of the path if we reach the end
        return drones

    # Assuming 'stemlines' is the LineCollection object from the initial ax.stem call
    def update_stemlines(stemlines, new_positions):
        segments = []
        for x, y, z in new_positions:
            segment = [(x, y, 0), (x, y, z)]  # Create a segment from base to drone
            segments.append(segment)
        stemlines.set_segments(segments)

    # Function to update the plot
    def update_plot(frame, plot, stemlines):
        update_stemlines(stemlines, drones[:, :3])
        plot.set_data(drones[:, 0], drones[:, 1])
        plot.set_3d_properties(drones[:, 2])
        return plot,

    # Creating animation
    ani = FuncAnimation(fig, update_plot, fargs=(plot, stemlines), frames=None, interval=20, blit=False, cache_frame_data=False)

    # Create a function which updates the positions of drones in a different thread
    def update_positions_thread():
        nonlocal stop_thread
        while True:
            update_positions(drones)
            time.sleep(0.01)
            if stop_thread:
                break

    # Start the thread
    i = 1
    stop_thread = False
    thread = threading.Thread(target=update_positions_thread)
    thread.start()

    plt.show()
    # Terminate the thread
    stop_thread = True  # Kill the thread once the plot is closed
    thread.join()

