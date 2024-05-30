#import the SceneBuilder class
from scenebuilder import SceneBuilder
#Create an instance of User Interface
gui = SceneBuilder()
#optionally set new limits for the square arena (applies both to x and y)
gui.set_lims((-1,1))
#Open the GUI
gui.draw_scene()