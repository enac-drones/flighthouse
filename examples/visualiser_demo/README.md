
# Visualiser Demos

Welcome to the Visualiser Demos! This directory contains three different visualisers to help you analyze drone flights. These visualisers allow you to see what drones did during their flights, providing valuable insights for analysis.

## Available Visualisers

1. **2D Visualiser**: 
   - This visualiser provides a simple 2D representation of the drone paths.
   - It's ideal for quickly viewing and analyzing flight patterns on a 2D plane.

2. **3D Visualiser with Dotted Lines**:
   - This visualiser shows the drone paths in 3D space with dotted lines connecting each drone to the ground.
   - It provides a clear visual representation of the drones' altitudes and movements in three dimensions.

3. **3D Visualiser with Semi-Transparent Sheets**:
   - This visualiser presents the drone paths in 3D space with semi-transparent sheets following behind each drone.
   - It's useful for visualizing the trajectory and flow of each drone's path over time.

## JSON Files

The visualisers use JSON files as input to plot the drone paths. You can choose between two types of JSON files:

1. **2D Simulated Flight**:
   - This file contains simulated flight data in 2D.
   - Use this to see how the visualiser works with basic, simulated flight patterns.

2. **3D Real Flight with Communication Gaps**:
   - This file contains real flight data in 3D, including communication gaps where drones might suddenly jump positions.
   - Use this to analyze real-world scenarios and understand how communication issues can affect drone flight paths.

## How to Run the Demos

1. Place the appropriate JSON file in the same directory as the demo script.
2. Run the corresponding demo script to visualize the drone paths:
   - For the 2D Visualiser: `python 2d_visualiser.py`
   - For the 3D Visualiser with Dotted Lines: `python 3d_dotted_visualiser.py`
   - For the 3D Visualiser with Semi-Transparent Sheets: `python 3d_sheets_visualiser.py`

Each script will load the JSON file, process the drone paths, and display the visualisation using Matplotlib.

We hope these visualisers help you gain valuable insights into your drone flights. Happy analyzing!
