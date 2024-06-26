from flighthouse import PlotTrajectories
import os

# First we determine where this script is and obtain the absolute file path to the output json file.
# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the JSON file
json_file_path = os.path.join(script_dir, 'pybullet_output.json')

'''note 'desired_vectors' parameter is optional in the json. If included, drones
will have an arrow pointed in that direction at each frame. There should be as many 
desired vectors as there are points in the path'''

if __name__ == "__main__":
    visualizer = PlotTrajectories(json_file_path, update_every=1)
    visualizer.show()