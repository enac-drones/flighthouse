from time import sleep
import time
import numpy as np

from djitellopy import TelloSwarm

from mocap.voliere import VolierePosition
from mocap.voliere import Vehicle
from mocap.voliere import Vehicle as Target

from pgflow import Cases
from pgflow import run_simulation, set_new_attribute
from pgflow import PlotTrajectories 
from pgflow import SimulationVisualizer

def main():

    file_name = 'voliere.json'
    case_name = '1v1b' # One Vehicle and One building

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
    case.mode = '' # None = clipped

    # ---------- OpTr- ACID - -----IP------
    ac_list = [
        # ["65", "65", "192.168.1.65"],
        # ["62", "62", "192.168.1.62"],
        ["69", "69", "192.168.1.69"],
    ]

    ip_list = [_[2] for _ in ac_list]
    swarm = TelloSwarm.fromIps(ip_list)

    id_list = [_[1] for _ in ac_list]
    for i, id in enumerate(id_list):
        swarm.tellos[i].set_ac_id(id)

    num_drones = len(id_list) # FIXME this should come from the case file !

    print("Connecting to Tello Swarm...")
    swarm.connect()
    print("Connected to Tello Swarm...")


    id_dict = dict([("69", "69"),
                    # ("69", "69"),
                    ])  # rigidbody_ID, aircraft_ID

    target_id_dict = dict([('888', '888')])
    # print('Dict keys : ',id_dict.keys())

    vehicles = dict((ac_id, swarm.tellos[i]) for i, ac_id in enumerate(id_dict.keys()))
    # vehicles = dict([(ac_id, Vehicle(ac_id)) for ac_id in id_dict.keys()])
    targets = dict([('888', Target('888'))]) # Helmet as a target

    voliere = VolierePosition(id_dict|target_id_dict, vehicles|targets, server='192.168.1.240', freq=100, vel_samples=6)
    # voliere = VolierePosition(ac_id_list, swarm.tellos+target+ball, freq=40)
    
    voliere.run()
    sleep(4) # Just giving some time for the OptiTrack to start...

    print("Starting Natnet3.x interface at %s" % ("1234567"))

    try:
        swarm.takeoff()

        # Simulation starts
        sim_start_time = starttime = time.time()
        
        while time.time() - sim_start_time < 18000:
            if time.time() - starttime > 0.099:
                starttime = time.time()

                # Target position acquisition
                target_pos = voliere.vehicles['888'].position
                # print(f' Target pos : {target_pos}')

                for j in range(num_drones):
                    case.vehicle_list[j].position = swarm.tellos[j].get_position_enu()
                    case.vehicle_list[j].velocity = swarm.tellos[j].get_velocity_enu()
                    # print(swarm.tellos[j].get_position_enu())

                """'Step the simulation by one timstep, list_of_vehicles is case.vehicle_list"""
                for j,vehicle in enumerate(case.vehicle_list):
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
                    vehicle.run_simple_sim(case.mode) # FIXME we are running unnneccessary position updates here. 
                    unit_vector = np.hstack((vehicle.run_flow_vel_calc_only(),0.0))
                    heading = 0.
                    heading = np.arctan2(unit_vector[1],unit_vector[0])

                    swarm.tellos[j].send_velocity_enu(unit_vector*0.8, heading)
                    

                # Directly fly to the point
                # for i, vehicle in enumerate(swarm.tellos):
                #     # swarm.tellos[i].fly_to_enu([i, i, 0.5], 0.0)

        #### Save the simulation results ###########################
        # log.save(flight_type='Tello')
        # log.save()

        # save simulation to output json file
        file_name = 'voliere_output.json'
        case.to_dict(file_path=file_name)

        swarm.move_down(int(40))
        swarm.land()
        voliere.stop()
        swarm.end()

    except (KeyboardInterrupt, SystemExit):
        print("Shutting down natnet interfaces...")
        # save simulation to output json file
        file_name = 'voliere_output.json'
        case.to_dict(file_path=file_name)
        

        swarm.move_down(int(40))
        swarm.land()
        voliere.stop()
        swarm.end()

        # Use the original visualiser
        trajectory_plot = PlotTrajectories(file_name, collision_threshold=0.5, max_connection_distance=case.max_avoidance_distance, update_every=1)

        # specify new axes plot limits if desired
        LIMS = (-5,5)
        trajectory_plot.ax.set_xlim(LIMS)
        trajectory_plot.ax.set_ylim(LIMS)
        # Show the trajectories
        trajectory_plot.show()

    except OSError:
        print("Natnet connection error")

        swarm.move_down(int(40))
        swarm.land()
        voliere.stop()
        swarm.end()
        exit(-1)


if __name__ == "__main__":
    main()