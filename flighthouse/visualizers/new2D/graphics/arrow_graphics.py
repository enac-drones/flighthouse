from ..entities.arrow import ArrowEntity
from matplotlib.patches import FancyArrow
from matplotlib.axes import Axes
import numpy as np
from numpy.typing import NDArray
from typing import List


class ArrowPatch:
    """
    Class containing an arrow patch
    """

    def __init__(self, arrow: ArrowEntity, **kwargs) -> None:
        self.arrow = arrow
        self.arrow_patch: FancyArrow = self.create_patch(**kwargs)

        pass

    def create_patch(self, **kwargs) -> FancyArrow:
        """
        Create a Arrow patch from the ArrowEntity

        Parameters:
        -----------
        arrow : ArrowEntity
            The arrow object to plot. This object should have 'start' and 'end' attributes
            which are [x, y] pairs defining the arrow's start and end.
        """
        arrow_ds: NDArray[np.float64] = np.array(self.arrow.end) - np.array(
            self.arrow.start
        )
        arrow_patch = FancyArrow(*self.arrow.start, *arrow_ds, **kwargs)
        return arrow_patch

    def get_patch(self):
        """
        Get the patch for the FancyArrow.

        Returns:
        --------
        patch : FancyArrow
            A matplotlib.patches.FancyArrow object representing the Arrow.
        """
        return self.arrow_patch

    def set_data(self, **kwargs):
        """
        Set FancyArrow x, y, dx, dy, width, head_with, and head_length. Values left as None will not be updated.
        Parameters:
        -----------
        **kwargs : dict
            The new attributes to set.
        """
        self.arrow_patch.set_data(**kwargs)

    def set_new_attributes(self, **kwargs):
        """
        This method allows the user to update the attributes of the FancyArrow

        Parameters:
        -----------
        **kwargs : dict
            The new attributes to set.
        """
        self.arrow_patch.set(**kwargs)


class ArrowPlotter:
    def __init__(self, case_data: dict):
        self.paths = []
        self.desired_vectors = []
        self.arrows: list = self._get_arrows_from_dict(case_data)
        self.arrow_patches: dict[str, ArrowPatch] = {}

    def plot(self, ax: Axes) -> None:
        """Plots the Arrows on the given Matplotlib Axes object.

        Parameters:
        -----------
        ax : Axes
            The Matplotlib Axes object to plot the Arrows on.

        Returns:
        --------
        None

        """
        for idx, arrow in enumerate(self.arrows):
            arrow_patch = ArrowPatch(arrow)
            self.arrow_patches[idx] = arrow_patch
            arrow_patch.create_patch()  # Initialize patches
            ax.add_artist(arrow_patch.get_patch())
            # ax.add_line(point_patch)

    def set_arrow_attributes(self, **kwargs):
        """
        Set the attributes of the building patches.

        Parameters:
        -----------
        kwargs : dict
            The keyword arguments to pass to the set_new_attributes() method of each BuildingPatch instance.
        """
        for arrow_patch in self.arrow_patches.values():
            arrow_patch.set_new_attributes(**kwargs)

    def set_data(self, **kwargs):
        """
        Set the attributes of the building patches.

        Parameters:
        -----------
        kwargs : dict
            The keyword arguments to pass to the set_new_attributes() method of each BuildingPatch instance.
        """
        for arrow_patch in self.arrow_patches.values():
            arrow_patch.set_data(**kwargs)

    def _get_arrows_from_dict(self, vehicle_data: List[dict]) -> List[ArrowEntity]:
        """
        Returns a list of arrows from a case data.

        Parameters:
        -----------
        desired_vectors : list
            A list of desired vectors, where each element is a dict with the desired vector's start and end.

        Returns:
        --------
        arrows : list of ArrowEntity objects
            A list of ArrowEntity objects extracted from the desired_vectors dictionary elements.
        """
        vehicle_positions = []
        # desired_vectors = []
        arrows: List[ArrowEntity] = []
        for vehicle in vehicle_data:
            vehicle_start = vehicle.get("path")[0][:2]
            vehicle_positions.append(np.array(vehicle_start))
            # desired_direction_2d = vehicle.get("gflow")[0][:2]
            self.desired_vectors.append(vehicle.get("desired_vectors"))
            self.paths.append(vehicle.get("path"))

        for idx, desired_vector in enumerate(self.desired_vectors):

            arrow = ArrowEntity(
                vehicle_positions[idx], vehicle_positions[idx] + desired_vector[0][:2]
            )
            arrows.append(arrow)

        # self.desired_vectors = desired_vectors
        return arrows

    def animate_arrows(self, frame: int, total_frames: int):
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
        longest_path = max(len(path) for path in self.paths)

        for idx, arrow_patch in self.arrow_patches.items():
            path = self.paths[idx]
            desired_vector = self.desired_vectors[idx]

            path_length = len(path)

            # Step 2: Calculate the number of frames for this drone
            drone_total_frames = int((path_length / longest_path) * total_frames)

            # Avoid division by zero for drones with no path
            if drone_total_frames == 0:
                continue

            # Step 3: Calculate the interpolated frame for this drone
            interpolated_frame = int((frame / drone_total_frames) * path_length)
            current_frame = min(interpolated_frame, path_length - 1)

            [new_x, new_y] = path[current_frame][:2]
            try:
                [new_dx, new_dy] = desired_vector[current_frame][:2]
            except IndexError:
                [new_dx, new_dy] = desired_vector[-1][:2]

            arrow_patch.set_data(x=new_x, y=new_y, dx=new_dx, dy=new_dy)
