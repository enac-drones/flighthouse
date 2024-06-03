"""Script demonstrating the dronesim integration
"""
import argparse
import time

import matplotlib.pyplot as plt
import numpy as np
import pybullet as p
import json
from scipy.spatial import ConvexHull
from dronesim.control.INDIControl import INDIControl
from dronesim.envs.BaseAviary import DroneModel, Physics
from dronesim.envs.CtrlAviary import CtrlAviary
from dronesim.utils.Logger import Logger
from dronesim.utils.utils import str2bool, sync

from PGFlow import Cases
from PGFlow.arena import ArenaMap
from PGFlow.utils.simulation_utils import step_simulation, set_new_attribute


# Create a PyBullet simulation environment
p.connect(p.GUI)

# Load polygons from the text file
with open("./building_12.json", "r") as f:
    # Load the JSON data
    data = json.load(f)

polygons = []
obstacles = data["scenebuilder"]["buildings"]
for id, obs in enumerate(obstacles): 
    floor = np.array(obs["vertices"]).copy() 
    floor[:,2] = 0.0
    ceil = np.array(obs["vertices"]).copy() 
    ceil[:,2] = 3.0
    
    tmp = np.vstack((floor, ceil))
    print(tmp)
    polygons.append(tmp)

# Create polygons in the simulation
for polygon_vertices in polygons:
    polygon_id = p.createCollisionShape(p.GEOM_MESH, vertices=polygon_vertices)
    p.createMultiBody(baseCollisionShapeIndex=polygon_id)


ArenaMap.size = 0.1
case = Cases.get_case('building_12.json', 'scenebuilder')
num_drones = len(case.vehicle_list)
case.mode = ''
set_new_attribute(case, 'source_strength', 3)

if __name__ == "__main__":

    #### Define and parse (optional) arguments for the script ##
    parser = argparse.ArgumentParser(
        description="Helix flight script using CtrlAviary or VisionAviary and DSLPIDControl"
    )
    parser.add_argument(
        "--drone",
        default=["robobee"]*num_drones, #hexa_6DOF_simple
        type=list,
        help="Drone model (default: CF2X)",
        metavar="",
        choices=[DroneModel],
    )
    parser.add_argument(
        "--num_drones",
        default=1,
        type=int,
        help="Number of drones (default: 3)",
        metavar="",
    )
    parser.add_argument(
        "--physics",
        default="pyb",
        type=Physics,
        help="Physics updates (default: PYB)",
        metavar="",
        choices=Physics,
    )
    parser.add_argument(
        "--vision",
        default=False,
        type=str2bool,
        help="Whether to use VisionAviary (default: False)",
        metavar="",
    )
    parser.add_argument(
        "--gui",
        default=True,
        type=str2bool,
        help="Whether to use PyBullet GUI (default: True)",
        metavar="",
    )
    parser.add_argument(
        "--record_video",
        default=False,
        type=str2bool,
        help="Whether to record a video (default: False)",
        metavar="",
    )
    parser.add_argument(
        "--plot",
        default=True,
        type=str2bool,
        help="Whether to plot the simulation results (default: True)",
        metavar="",
    )
    parser.add_argument(
        "--user_debug_gui",
        default=False,
        type=str2bool,
        help="Whether to add debug lines and parameters to the GUI (default: False)",
        metavar="",
    )
    parser.add_argument(
        "--aggregate",
        default=True,
        type=str2bool,
        help="Whether to aggregate physics steps (default: True)",
        metavar="",
    )
    parser.add_argument(
        "--obstacles",
        default=False,
        type=str2bool,
        help="Whether to add obstacles to the environment (default: True)",
        metavar="",
    )
    parser.add_argument(
        "--simulation_freq_hz",
        default=240,
        type=int,
        help="Simulation frequency in Hz (default: 240)",
        metavar="",
    )
    parser.add_argument(
        "--control_freq_hz",
        default=96,
        type=int,
        help="Control frequency in Hz (default: 48)",
        metavar="",
    )
    parser.add_argument(
        "--duration_sec",
        default=20,
        type=int,
        help="Duration of the simulation in seconds (default: 5)",
        metavar="",
    )
    ARGS = parser.parse_args()

    #### Initialize the simulation #############################
    H = 0.50
    H_STEP = 0.05
    R = 2

    AGGR_PHY_STEPS = (
        int(ARGS.simulation_freq_hz / ARGS.control_freq_hz) if ARGS.aggregate else 1
    )

    
    ## Hover ###
    # INIT_XYZS = np.array([[0.0, 0.0, 0.6]])
    INIT_XYZS = np.array([v.position for v in case.vehicle_list])
    rpy = [0.0, 0.0 * 3.14 / 180.0, 0.0 * 3.14 / 180.0]
    INIT_RPYS = np.array([rpy for _ in range(num_drones)])
    vel = [0.0, 0.0, 0.0]
    INIT_VELS = np.array([vel for _ in range(num_drones)])

    #### Initialize a circular trajectory ######################
    PERIOD = 15
    NUM_WP = ARGS.control_freq_hz * PERIOD

    TARGET_POS = np.zeros((NUM_WP, 3))
    for i in range(NUM_WP):
        TARGET_POS[i, :] = (
            R * np.cos((i / NUM_WP) * (4 * np.pi) + np.pi / 2) + INIT_XYZS[0, 0],
            R * np.sin((i / NUM_WP) * (4 * np.pi) + np.pi / 2) - R + INIT_XYZS[0, 1],
            0,
        )

    TARGET_RPYS = np.zeros((NUM_WP, 3))
    for i in range(NUM_WP):
        TARGET_RPYS[i, :] = [0.0, 0.0, 0.0]  # 0.4+(i*1./200)]

    #### Create the environment ##
    env = CtrlAviary(
        drone_model=ARGS.drone,
        num_drones=num_drones,
        initial_xyzs=INIT_XYZS,
        initial_vels=INIT_VELS,
        initial_rpys=INIT_RPYS,
        physics=ARGS.physics,
        neighbourhood_radius=10,
        freq=ARGS.simulation_freq_hz,
        aggregate_phy_steps=AGGR_PHY_STEPS,
        gui=ARGS.gui,
        record=ARGS.record_video,
        obstacles=ARGS.obstacles,
        user_debug_gui=ARGS.user_debug_gui,
    )

    #### Obtain the PyBullet Client ID from the environment ####
    PYB_CLIENT = env.getPyBulletClient()

    #### Initialize the logger #################################
    logger = Logger(
        logging_freq_hz=int(ARGS.simulation_freq_hz / AGGR_PHY_STEPS),
        num_drones=num_drones,
    )

    #### Initialize the controllers ############################
    ctrl = [INDIControl(drone_model=drone) for drone in ARGS.drone]

    #### Run the simulation ####################################
    CTRL_EVERY_N_STEPS = int(np.floor(env.SIM_FREQ / ARGS.control_freq_hz))
    action = {
        str(i): np.array([0.3, 0.3, 0.3, 0.3]) for i in range(num_drones)
    }
    # action = {'0': np.array([0.5,0.5,0.5,0.5,0.5,0.5])}# , '1': np.array([0.5,0.5,0.5,0.5])}
    START = time.time()
    for i in range(0, int(ARGS.duration_sec * env.SIM_FREQ), AGGR_PHY_STEPS):

        #### Step the simulation ###################################
        obs, reward, done, info = env.step(action)

        for j in range(num_drones):
            # print(f"{obs[str(j)]["state"]}")
            pos = obs[str(j)]["state"][:3]
            case.vehicle_list[j].position = pos
        step_simulation(case)

        #### Compute control at the desired frequency ##############
        if i % CTRL_EVERY_N_STEPS == 0:
            #### Compute control for the current way point #############
            for j in range(num_drones):

                vehicle = case.vehicle_list[j]
                if vehicle.state==1:
                    desired_vector = np.array([0,0,-1])
                else:
                    desired_vector = vehicle.desired_vectors[-1]
                    desired_vector = np.hstack([desired_vector, 0])

               
                
                action[str(j)], _, _ = ctrl[j].computeControlFromState(
                        control_timestep=CTRL_EVERY_N_STEPS * env.TIMESTEP,
                        state=obs[str(j)]["state"],
                        target_pos = np.hstack([obs[str(j)]["state"][:2], 0.5]),
                        target_vel=desired_vector*0.6,
                        # target_acc=np.zeros(3),
                        # target_rpy=np.zeros(3),
                        # target_rpy_rates=np.zeros(3),
                    )
         
        #### Printout ##############################################
        if i % env.SIM_FREQ == 0:
            env.render()

        #### Sync the simulation ###################################
        if ARGS.gui:
            sync(i, START, env.TIMESTEP)

        ### Break the simulation if we are close to ground
        # if z < 0.3:
        #     break
    #### Close the environment #################################
    env.close()
    case.to_dict('pybullet_output.json')

    #### Save the simulation results ###########################
    # logger.save()

    #### Plot the simulation results ###########################
    # if ARGS.plot:
    #     logger.plot()
