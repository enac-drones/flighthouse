import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from matplotlib.axes import Axes
from typing import List

# import Drone class
from ..entities.drone import DroneEntity
from ..entities.path import PathEntity


class DronePatch:
    """
    Represents the visual representation of a drone as a patch in Matplotlib.

    Attributes:
    -----------
    drone : Drone
        The drone object to be visualized.
    point_color : str
        The color of the point representing the drone's center.
    circle_color : str
        The color of the circle representing the drone's detection radius.
    circle_width : float
        The line width of the circle.
    """

    def __init__(
        self,
        drone: DroneEntity,
        point_color: str = "k",
        circle_color="k",
        circle_width=0.5,
        marker="o",
        markersize: float = 2,
    ):

        self.drone = drone
        self.point_color = point_color
        self.circle_color = circle_color
        self.circle_width = circle_width
        self.marker = marker
        self.markersize = markersize

    def create_patches(self) -> None:
        # Create the central point
        self.point = plt.Line2D(
            [self.drone.position[0]],
            [self.drone.position[1]],
            color=self.point_color,
            marker=self.marker,
            markersize=self.markersize,
            animated=False,
        )

        # Create the detection circle
        self.circle = Circle(
            self.drone.position,
            self.drone.radius,
            edgecolor=self.circle_color,
            facecolor="none",
            linewidth=self.circle_width,
            animated=False,
        )

        return None

    def get_circle_patch(self) -> Circle:
        return self.circle

    def get_point_patch(self) -> Line2D:
        return self.point

    def set_circle_attributes(self, **kwargs) -> None:
        """
        Sets the attributes of the circle around the drone.
        Refer to matplolib.patches.Circle for viable keyword arguments
        """
        circle = self.get_circle_patch()
        circle.set(**kwargs)

    def set_point_attributes(self, **kwargs) -> None:
        """
        Sets the attributes of the central point of the drone.
        Refer to matplolib.lines.Line2D for viable keyword arguments
        """
        point = self.get_point_patch()
        point.set(**kwargs)

    def set_position(self, x: float, y: float) -> None:
        """
        Sets the position of the drone.
        """
        self.drone.position = [x, y]
        self.point.set_data([x], [y])
        self.circle.center = (x, y)
        return None


class DronePlotter:
    """
    A class for plotting multiple drones on a Matplotlib figure.

    Attributes:
    -----------
    drones : list of Drone
        A list of drone objects to be plotted.
    point_color : str
        The color of the points representing the drones' centers.
    circle_color : str
        The color of the circles representing the drones' detection radii.
    circle_width : float
        The line width of the circles.
    """

    def __init__(
        self, vehicle_data: list[dict], point_color="blue", circle_color="red"
    ):

        self.drones: list[DroneEntity] = self._get_drones_from_dict(vehicle_data)
        self.drone_patches: dict[str, DronePatch] = {}
        self.point_color = point_color
        self.circle_color = circle_color
        self.circle_width: float = 2.0

    def plot(self, ax: Axes) -> None:
        """Plots the drones on the given Matplotlib Axes object.

        Parameters:
        -----------
        ax : Axes
            The Matplotlib Axes object to plot the drones on.

        Returns:
        --------
        None

        """
        for drone in self.drones:
            drone_patch = DronePatch(
                drone, self.point_color, self.circle_color, self.circle_width
            )
            self.drone_patches[drone.id] = drone_patch
            drone_patch.create_patches()  # Initialize patches
            circle_patch = drone_patch.get_circle_patch()
            point_patch = drone_patch.get_point_patch()
            ax.add_patch(circle_patch)
            ax.add_line(point_patch)

    def animate_drones(self, frame: int, total_frames: int):
        """
        Animates the drones along their paths.

        Parameters:
        -----------
        frame : int
            The current frame number.
        total_frames : int
            The total number of frames to animate.
        """
        # Step 1: Find the longest path
        longest_path = max(
            len(drone_patch.drone.path) for drone_patch in self.drone_patches.values()
        )

        for drone_patch in self.drone_patches.values():
            path_length = len(drone_patch.drone.path)

            # Step 2: Calculate the number of frames for this drone
            drone_total_frames = int((path_length / longest_path) * total_frames)

            # Avoid division by zero for drones with no path
            if drone_total_frames == 0:
                continue

            # Step 3: Calculate the interpolated frame for this drone
            interpolated_frame = int((frame / drone_total_frames) * path_length)
            current_frame = min(interpolated_frame, path_length - 1)

            drone_patch.set_position(*drone_patch.drone.path[current_frame])

    def _get_drones_from_dict(self, vehicle_data: list[dict]) -> List[DroneEntity]:
        """
        Returns a list of drones from a list of vehicle data.

        Parameters:
        -----------
        vehicle_data : list
            A list of vehicle data, where each element is a dict with the vehicle's id and path.

        Returns:
        --------
        drones : list of DroneEntity objects
            A list of DroneEntity objects extracted from the vehicle_data dictionary elements.
        """
        drones: List[DroneEntity] = []
        for vehicle in vehicle_data:
            path_2d = [tuple(p[:2]) for p in vehicle["path"]]
            drone = DroneEntity(
                position=path_2d[0],
                goal=path_2d[-1],
                radius=vehicle.get("radius", 0.5),
                path=path_2d,
            )
            drones.append(drone)
        return drones

    def set_circle_attributes(self, **kwargs) -> None:
        """
        Sets the attributes of the circles around the drones.

        Parameters:
        -----------
        **kwargs : keyword arguments
            Keyword arguments to pass to the Circle.set() method.

        Returns:
        --------
        None

        """
        for drone_patch in self.drone_patches.values():
            drone_patch.set_circle_attributes(**kwargs)
        return None

    def set_point_attributes(self, **kwargs) -> None:
        """
        Sets the attributes of the central points of the drones.

        Parameters:
        -----------
        **kwargs : keyword arguments
            Keyword arguments to pass to the Line2D.set() method.

        Returns:
        --------
        None

        """
        for drone_patch in self.drone_patches.values():
            drone_patch.set_point_attributes(**kwargs)
        return None

    def get_patches(self) -> List:
        """
        Returns a list of patches representing the drones.
        """
        patches = []
        for drone_patch in self.drone_patches.values():
            patches.append(drone_patch.get_circle_patch())
            patches.append(drone_patch.get_point_patch())

        return patches
