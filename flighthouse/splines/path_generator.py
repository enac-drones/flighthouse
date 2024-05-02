import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # Correct import for Poly3DCollection
# #create the basis coefficient matrices
# #spline types: Bezier, BSpline, Catmull-Rom
# #create a json file to store the basis matrices for each of the above splines
# minvo3 = np.array([
#     [-0.4302, 0.4568, -0.02698, 0.0004103],
#     [0.8349, -0.4568, -0.7921, 0.4997],
#     [-0.8349, -0.4568, 0.7921, 0.4996],
#     [0.4302, 0.4568, 0.02698, -0.0004103]
# ]).T

# bezier3 = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0],[1, 0, 0, 0]])
# #random four points in space
# points = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]])
# hull = ConvexHull(points)

# def draw_spline(t:float):
#     # print(t)
#     T = np.array([t**3, t**2, t, 1])
#     MP = minvo3@points
#     P = T@MP
#     return P

# t_values = np.linspace(-1, 1, 100)
# spline_points = np.array([draw_spline(t) for t in t_values])

# ax = plt.figure().add_subplot(projection='3d')
# #draw the hull
# # Plotting the convex hull
# ax.scatter(points[:, 0], points[:, 1], points[:, 2], edgecolors='k')
# for simplex in hull.simplices:
#     # Extract the vertices for each simplex (face of the tetrahedron)
#     simplex = np.append(simplex, simplex[0])  # loop back to first vertex
#     # Fill the face with a translucent color
#     triangle = points[simplex[:3]]
#     ax.add_collection3d(Poly3DCollection([triangle], ec = 'k', fc='cyan', alpha=0.1))  # adjust alpha for translucency

# ax.plot(spline_points[:,0], spline_points[:,1],spline_points[:,2])
# plt.show()




#create the basis coefficient matrices
#spline types: Bezier, BSpline, Catmull-Rom
#create a json file to store the basis matrices for each of the above splines

#original minvo from the paper which works for t values of -1  to 1
minvo3 = np.array([
    [-0.4302, 0.4568, -0.02698, 0.0004103],
    [0.8349, -0.4568, -0.7921, 0.4997],
    [-0.8349, -0.4568, 0.7921, 0.4996],
    [0.4302, 0.4568, 0.02698, -0.0004103]
]).T

#modified minvo to work with t from 0 to 1 like most other splines
minvo3 = np.array([
    [-3.4416, 6.9896, -4.46236, 0.91439], 
    [6.6792, -11.846, 5.2524, 0.0001],
    [-6.6792, 8.1916, -1.598, 0.0856],
    [3.4416, -3.3352, 0.80796, -0.0007903]
]).T

# t = -1
# print(np.array([t**3, t**2, t, 1])@minvo3)
# t = 0
# print(np.array([t**3, t**2, t, 1])@minvo3_1)
bezier3 = np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0], 
    [-3, 3, 0, 0],
    [1, 0, 0, 0]])

bspline3 = np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 0, 3, 0],
    [1, 4, 1, 0]]) / 6
#random four points in space
points = np.array([[0,0],[0,0],[0,0],[1,1], [2,0],[3,2], [4,4], [5.2,3], [6,0],[6.8,-3], [8,0], [9.5,-2],[9.5,-2],[9.5,-2]])
# points = np. array([[3,1],[3,1],[3,1],[8,-2]])

def draw_spline(t:float, points:np.ndarray):
    # print(t)
    T = np.array([t**3, t**2, t, 1])
    MP = bspline3@points
    P = T@MP
    return P
# print(points[:-1].shape, points[:-1])
t_values = np.linspace(0, 1, 100)
for i in range(len(points)-3):
    spline_points = np.array([draw_spline(t, points[i:i+4]) for t in t_values])
    plt.plot(spline_points[:,0], spline_points[:,1])

#convert between spline control points
# minvo_points = np.linalg.inv(minvo3)@bspline3@points
# plt.plot(minvo_points[:, 0], minvo_points[:, 1], 'o')
plt.plot(points[:, 0], points[:, 1], 'o')
plt.show()