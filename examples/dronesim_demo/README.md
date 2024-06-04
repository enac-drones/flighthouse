# Dronesim Simulation and Visualisation using Pybullet

### Installation of additional dependencies
#### 1. dronesim (pybullet drone simulator)

From source:

`git clone git@github.com:enac-drones/dronesim.git`

`cd dronesim`

`pip install -e .`

#### 2. PGFlow (multi agent path planne based on artificial potential fields). This is required only for the demo; if you wish to test your own algorithms, it is not required.

With pip (recommended):

`pip install pgflow`

From source:

`https://github.com/enac-drones/PGFlow`

`cd pgflow`

`pip install -e .` 

## Running the simulation

Ensure dronesim and pgflow have been installed into your virtual environment.

`cd flighthouse/examples/dronesim_demo/`

`python3 dronesim_example.py`

