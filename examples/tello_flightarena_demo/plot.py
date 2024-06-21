from pgflow import PlotTrajectories 

file_name = 'voliere_output.json'

# Use the original visualiser
trajectory_plot = PlotTrajectories(file_name, collision_threshold=0.5, max_connection_distance=5., update_every=1)

# specify new axes plot limits if desired
LIMS = (-5,5)
trajectory_plot.ax.set_xlim(LIMS)
trajectory_plot.ax.set_ylim(LIMS)
# Show the trajectories
trajectory_plot.show()