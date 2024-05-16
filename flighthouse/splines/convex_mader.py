import numpy as np
from scipy.optimize import minimize

bspline3 = np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 0, 3, 0],
    [1, 4, 1, 0]]) / 6

bezier3 = np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0], 
    [-3, 3, 0, 0],
    [1, 0, 0, 0]])


def calculate_effort(points):
    jerk_matrix = np.array([[6,0,0,0]])
    jerk = jerk_matrix@bezier3@points
    return np.linalg.norm(jerk)**2


# Define the objective function to minimize jerk
# Objective function: sum of squares of the equations
def objective(control_points):
    points = np.array(control_points).reshape((4,-1))
    effort = calculate_effort(points)
    # Your equations here, corrected to return the sum of squares
    return effort

#define plane characteristics n and d
n = np.array([0, 1, 1])
d = 1
# Define the constraint function to enforce points lying on one side of the plane
def plane_constraint(control_points):
    # Assuming control_points is a 2D array with shape (4, 3) representing 4 control points in 3D space
    # Calculate the dot product of each control point with the normal vector and add the distance
    distances_to_plane = np.dot(control_points.reshape(-1,3), n) + d
    # Return a 1D array with the constraint equation for each control point
    return distances_to_plane

# Define initial guess for control point positions
x1, y1, z1 = 0, 0, 0
x2, y2, z2 = 1, 0, 0
x3, y3, z3 = 1, 1, 0
x4, y4, z4 = 0, 1, 0
# Define initial guess for control point positions as a flattened 1D array
initial_guess = np.array([x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4])

# Define the constraint dictionary for scipy.optimize.minimize
constraints = [{'type': 'ineq', 'fun': plane_constraint}]
# Define the options dictionary for scipy.optimize.minimize
options = {'disp': True}  # Display optimization progress

# Use scipy.optimize.minimize to find the optimal positions of the control points
result = minimize(objective, initial_guess, constraints=constraints, options=options)


# Optimal positions of the control points
optimal_control_points = result.x.reshape((4, 3))
print(optimal_control_points)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Plot the separating plane
xx, yy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
z = (-n[0] * xx - n[1] * yy - d) * 1. /n[2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xx, yy, z, alpha=0.5)

# Plot the control points
control_points = result.x.reshape((4, 3))
ax.scatter(control_points[:, 0], control_points[:, 1], control_points[:, 2], c='r', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
#set the x y and z limits to -2 to 2
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

plt.show()
