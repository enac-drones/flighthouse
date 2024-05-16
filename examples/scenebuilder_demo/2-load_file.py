import os
from scenebuilder import SceneBuilder

# Get the directory in which this script is located
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create an instance of User Interface
plot = SceneBuilder()

# Specify a JSON or GeoJSON file with a pre-existing scene
# Use os.path.join to construct the full path to the file
scene_file = os.path.join(dir_path, 'scenebuilder.json')
plot.load_scene(scene_file)

# Open the GUI
plot.draw_scene()
