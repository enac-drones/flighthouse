import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # Correct import for Poly3DCollection
#create the basis coefficient matrices
#spline types: Bezier, BSpline, Catmull-Rom
#create a json file to store the basis matrices for each of the above splines
minvo3 = np.array([
    [-0.4302, 0.4568, -0.02698, 0.0004103],
    [0.8349, -0.4568, -0.7921, 0.4997],
    [-0.8349, -0.4568, 0.7921, 0.4996],
    [0.4302, 0.4568, 0.02698, -0.0004103]
]).T

bezier3 = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0],[1, 0, 0, 0]])
#random four points in space
points = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]])
hull = ConvexHull(points)

def draw_spline(t:float):
    # print(t)
    T = np.array([t**3, t**2, t, 1])
    MP = minvo3@points
    P = T@MP
    return P

t_values = np.linspace(-1, 1, 100)
spline_points = np.array([draw_spline(t) for t in t_values])

ax = plt.figure().add_subplot(projection='3d')
#draw the hull
# Plotting the convex hull
ax.scatter(points[:, 0], points[:, 1], points[:, 2], edgecolors='k')
for simplex in hull.simplices:
    # Extract the vertices for each simplex (face of the tetrahedron)
    simplex = np.append(simplex, simplex[0])  # loop back to first vertex
    # Fill the face with a translucent color
    triangle = points[simplex[:3]]
    ax.add_collection3d(Poly3DCollection([triangle], ec = 'k', fc='cyan', alpha=0.1))  # adjust alpha for translucency

ax.plot(spline_points[:,0], spline_points[:,1],spline_points[:,2])
plt.show()