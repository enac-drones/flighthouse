#import the SceneBuilder class
from scenebuilder import SceneBuilder
#Create an instance of User Interface
gui = SceneBuilder()
# optionally set new limits in meters for the square arena (applies both to x and y)
# the default is (-5,5)
gui.set_lims((-10,10))
#Open the GUI.
gui.draw_scene()