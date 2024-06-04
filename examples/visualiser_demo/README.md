
# Visualiser Demos

Welcome to the Visualiser Demos! This directory contains three different visualisers to help you analyze drone flights. These visualisers allow you to see what drones did during their flights, acting as a useful tool to iterate on your path planning algorithms.

## Available Visualisers

1. **2D Visualiser with Slider**: 
   - This is the first of two 2D visualisers, called SimulationVisualiser.
   - This visualiser provides a simple 2D representation of the drone paths, as if viewed from above. 
   - The visualiser will ignore the $z$ coordinate (if it exists) of both buildings and drones.
   - A slider is provided for detailed analysis of the trajectories

2. **Second 2D Visualiser with Slider**: 
   - This is the second of two 2D visualisers, called PlotTrajectories. It differs from the first mostly aesthetically. There is also the option to set the parameter max_connection_distance which will connect drones that are closer than this distance to each other with a black line, which gets thicker the closer they are.

2. **3D Visualiser with Paths and Optional Semi-Transparent Sheets**:
   - This visualiser shows an animation of the drone paths in 3D space with semi-transparent sheets extending from the path line to the ground.
   - Rendering the sheets can be expensive, so the user can choose not to display them (the path line will remain visible)
   - The user can change the time interval (in ms) between frames to slow down the animation
   - The user can change the history length. This is how many past time steps to include in the animation.
   - Due to matplotlib limitations, drones will always be rendered behind the buildings. To make this less noticeable, the buildings are made slightly transparent. 
<!-- 
3. **Real Time 3D Visualiser**:
   - This uses threading to display drone positions in real time. TODO using pybullet DroneSim. -->

## JSON Files

The visualisers use JSON files as input to plot the drone paths. These are identical for 2D or 3D plotting. The following JSON files are provided in the demos:
- ***simulated_flight.json***: data from a flight simulated with our in-house PGFlow guidance algorithm and several obstacles.
- ***real_flight.json*** data from a real flight flow in our drone arena. This contains evidence of communications issues with the drones, as they can be sometimes seen jumping to new positions after stopping for a short amounbt of time


## How to Run the Demos

1. Ensure the JSON files are in the same directory as the demo scripts.
2. Run the corresponding demo script to visualize the drone paths:
   - For the 2D Visualisers: `python3 demo2D_1.py` or `python3 demo2D_2.py`
   - For the 3D Visualiser with Semi-Transparent Sheets: `python3 demo3D.py`

Each script will load the JSON file, process the drone paths, and display the visualisation using Matplotlib.

We hope these visualisers help you gain valuable insights into your drone flights. Happy analyzing!
