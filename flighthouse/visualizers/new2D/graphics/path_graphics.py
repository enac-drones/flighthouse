import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from ..entities.path import PathEntity
from matplotlib.lines import Line2D
from typing import List


class PathPatch:
    """
    Represents the visual representation of a drone's path as a line in Matplotlib.

    Attributes:
    -----------
    path_entity : PathEntity
        The path entity to be visualized.
    line_color : str
        The color of the path line.
    line_width : float
        The width of the path line.
    """

    def __init__(self, path_entity: PathEntity, line_color="blue", line_width=2.0):
        self.path_entity = path_entity
        self.line_color = line_color
        self.line_width = line_width
        self.line = None

    def create_patch(self, ax: Axes) -> Line2D:
        """Create the path line on the given Matplotlib Axes object."""
        x_coords, y_coords = zip(*self.path_entity.path)
        (self.line,) = ax.plot(
            x_coords, y_coords, color=self.line_color, linewidth=self.line_width
        )
        return self.line

    def set_path_attributes(self, **kwargs):
        """Set the attributes of the path line."""
        self.line.set(**kwargs)
        return None


class PathPlotter:
    """
    Manages and plots the paths of multiple drones.

    Attributes:
    -----------
    paths : List[PathEntity]
        A list of path entities to be visualized.
    """

    def __init__(self, vehicle_data: List[dict]):
        self.paths = [
            PathEntity([tuple(p[:2]) for p in vehicle["path"]])
            for vehicle in vehicle_data
        ]

        self.path_patches: List[PathPatch] = []

    def plot(self, ax: Axes, line_color="gray", line_width=1.0):
        """Create and store PathPatch instances for each path."""
        for path in self.paths:
            path_patch = PathPatch(path, line_color, line_width)
            path_patch.create_patch(ax)
            self.path_patches.append(path_patch)

    def set_path_attributes(self, **kwargs):
        """
        Set the attributes of the path lines.

        Parameters:
        -----------
        kwargs : dict
            The keyword arguments to pass to the set_path_attributes() method of each PathPatch instance.
            Allowable kwargs are the same as those for matplotlib.lines.Line2D

        Returns:
        --------
        None

        Notes:
        ------
        This method is a wrapper around the set_path_attributes() method of each PathPatch instance.
        It iterates through the list of PathPatch instances and calls set_path_attributes() on each one.

        This allows the PathManager to set the attributes of the path lines independently of the PathPatch instances.
        For example, if the line color is changed for all paths, the PathManager can call set_path_attributes()
        with the new color as a keyword argument. This will set the color of all the path lines.

        The set_path_attributes() method of each PathPatch instance will then update the attributes of the path line.

        This allows the PathManager to set the attributes of the path lines independently of the PathPatch instances.
        """
        for path_patch in self.path_patches:
            path_patch.set_path_attributes(**kwargs)
        return None
