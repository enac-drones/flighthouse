import os
from scenebuilder import SceneBuilder

# Create an instance of User Interface
gui = SceneBuilder()

# Get the directory in which this script is located
dir_path = os.path.dirname(os.path.realpath(__file__))

# Specify a JSON or GeoJSON file with a pre-existing scene
# TODO uncomment one of the two lines below to pick a json or geojson file to load.

file = "pentagon.json"
# file = "pentagon.geojson"


# Use os.path.join to construct the full path to the file
scene_file = os.path.join(dir_path, file)
gui.load_scene(scene_file)

# Uncomment the line below to set new limits
# gui.set_lims((-10,10))

# Open the GUI
gui.draw_scene()
