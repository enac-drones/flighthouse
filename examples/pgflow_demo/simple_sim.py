from pgflow import Cases
from pgflow import run_simulation, set_new_attribute
from flighthouse import SimulationVisualizer
from flighthouse import SceneBuilder


''' 
The two lines below open the SceneBuilder GUI. Once you are finished drawing your
scene, save it in DEFAULT JSON format and close the GUI. PGFLow does not support GeoJSON
Make sure to use the default file name: scenebuilder.json
Save it to the directory containing this example
'''
# Open the SceneBuilder GUI
p = SceneBuilder()
p.draw_scene() 

#select the output file
file_name = 'scenebuilder.json'

''' 
NOTE The default json format currently supports having multiple cases in one json file.
This may be confusing in the future, but for now we must specify a case name for gflow
to select the correct one. SceneBuilder always saves cases with the name "scenebuilder".
If you type in the wrong case_name below, you will simply be prompted by PGFlow to type the correct one
in the command line interface.
'''
case_name="scenebuilder"

'''
NOTE the entire section below is specific to our algorithm PGFlow, you could bypass it with
your own algorithm
'''

############################  START OF PGFLOW  #################################################
'''
This is where your algorithm would go. PGFlow operates with objects of its Case class. A case
contains all information about a scenario, including vehicles, buildings, paths etc. PGFlow has 
a class method Cases.get_case which takes a json file and case name as input and creates an instance 
of a Case object. PGFlow has the set_new_attribute method which allows you to modify certain parameters
of the Vehicle class that are specific to our algorithm (such as max_speed for the vehicles etc).
You can ignore these lines. 
'''
case = Cases.get_case(file_name, case_name)

# setting some parameters for our algorithm
set_new_attribute(case, "sink_strength", new_attribute_value=5)
set_new_attribute(case, "max_speed", new_attribute_value=0.5)
set_new_attribute(case, "imag_source_strength", new_attribute_value=1)
set_new_attribute(case, "source_strength", new_attribute_value=1)
set_new_attribute(case,"v_free_stream_mag", new_attribute_value=0.0)
set_new_attribute(case,"ARRIVAL_DISTANCE", new_attribute_value=0.1)
# set_new_attribute(case, "turn_radius", new_attribute_value=0.05)

'''
PGFlow can also set parameters by directly modifying existing ones in a Case instance. These determine
various variables, such the maximum distance between a pair of vehicles above which they no longer "see"
each other and the threshold to a building's bounding box, above which it will no longer be 'detected'. 
Again, you can disregard these parameters as they are specific to each algorithm
'''
case.max_avoidance_distance = 5
case.building_detection_threshold = 1
case.mode = ''

'''
Finally PGFlow has a run_simulation method which takes the max number of timesteps, whether to stop the
simulation if a collision is detected and a parameter that represents how many timesteps elapse between 
drone communications: ie if update_every is set to 10, drones will only be updated about each others' 
positions every 10 timesteps in the simulation.
'''

result = run_simulation(
    case,
    t=1500,
    update_every=1,
    stop_at_collision=False
    )

'''
Once the simulation is over, PGFlow has a method to save the resulting paths along with the obstacle 
locations to the JSON format compatible with FLightHouse's visualisers.
'''

# create ouput json
case.to_dict(file_path="pgflow_output.json")

############################  END OF PGFLOW  #################################################


# visualisation
visualizer = SimulationVisualizer('pgflow_output.json')
visualizer.show_plot()