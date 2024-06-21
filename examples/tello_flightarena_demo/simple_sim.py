import time
from pgflow import Cases
from pgflow import run_simulation, set_new_attribute
from pgflow import PlotTrajectories 
from pgflow import SimulationVisualizer

file_name = 'voliere.json'
case_name = '1v1b'

case = Cases.get_case(file_name, case_name)
set_new_attribute(case, "sink_strength", new_attribute_value=5)
set_new_attribute(case, "max_speed", new_attribute_value=0.5)
set_new_attribute(case, "imag_source_strength", new_attribute_value=1)
set_new_attribute(case, "source_strength", new_attribute_value=1)
set_new_attribute(case, "v_free_stream_mag", new_attribute_value=0.0)
set_new_attribute(case, "ARRIVAL_DISTANCE", new_attribute_value=0.1)
set_new_attribute(case, "turn_radius", new_attribute_value=0.05)
case.max_avoidance_distance = 5
case.building_detection_threshold = 10
case.mode = ''

print(f'Building vertices : {case.buildings[0].vertices}')
print(f'Building vertices : {case.buildings[0].mplPoly}')
print(f'Building vertices : {case.buildings[0].shapelyPoly}')

stop_at_collision = False
update_every = 1

start_time = time.perf_counter()
for i in range(1000):
    # Step the simulation
    """'Step the simulation by one timstep, list_of_vehicles is case.vehicle_list"""
    for vehicle in case.vehicle_list:
        if case.arena.contains_point(vehicle.position[:2]):
            pass
        # if the current vehicle has arrived, do nothing, continue looking at the other vehicles
        if vehicle.state == 1:
            vehicle.desired_vectors.append([0,0])
            continue
        # update the vehicle's personal knowledge of other drones by only keeping those that meet specific conditions:
        # not too far, have not arrived yet, and are transmitting.
        # NOTE order matters, update buildings before vehicles
        vehicle.update_nearby_buildings(threshold=case.building_detection_threshold)  # meters
        vehicle.update_personal_vehicle_dict(case.vehicle_list, case.max_avoidance_distance)

        # update my position in the case_vehicle_list
        vehicle.run_simple_sim(case.mode)

    if case.colliding():
        # a collision has been detected, do whatever you want
        collisions = True
        if stop_at_collision:
            print(f'Collision detected at timestep {i}')
            exit()
    # Communication Block
    for vehicle in case.vehicle_list:
        if i % update_every == 0:
            vehicle.transmitting = True
        else:
            vehicle.transmitting = False

end_time = time.perf_counter()
print(f"Simulation took {end_time - start_time} seconds")


# save simulation to output json file
file_name = 'example_output.json'
case.to_dict(file_path=file_name)

# Use the original visualiser
trajectory_plot = PlotTrajectories(file_name, collision_threshold=0.5, max_connection_distance=case.max_avoidance_distance, update_every=1)

# specify new axes plot limits if desired
LIMS = (-5,5)
trajectory_plot.ax.set_xlim(LIMS)
trajectory_plot.ax.set_ylim(LIMS)
# Show the trajectories
trajectory_plot.show()


# Use the alternative visualiser
visualizer = SimulationVisualizer(file_name)
visualizer.show_plot()
