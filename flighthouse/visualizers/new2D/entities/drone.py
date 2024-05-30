from numpy.typing import NDArray
from numpy import float64
from typing import List

Point2D = NDArray[float64]


class DroneEntity:
    """
    Represents a drone with a position and a collision radius.

    Attributes:
    -----------
    position : tuple of float
        The (x, y) coordinates of the drone's position.
    radius : float
        The radius of the collision circle around the drone.
    """

    _id_counter = 0

    def __init__(
        self, position: Point2D, goal: Point2D, path: NDArray, radius: float = 0.2
    ):
        """
        Initializes a DroneEntity object.

        Parameters:
        -----------
        position : tuple of float
            The (x, y) coordinates of the drone's position.
        goal : tuple of float
            The (x, y) coordinates of the goal.
        path : numpy.ndarray
            The path of the drone.
        radius : float
            The radius of the collision circle around the drone.
        """
        self.id: str = f"V{DroneEntity._id_counter}"
        DroneEntity._id_counter += 1
        self.position = position
        self.goal = goal
        self.path = path
        self.radius = radius

    def __repr__(self):
        return f"Drone(position={self.position}, goal={self.goal})"
