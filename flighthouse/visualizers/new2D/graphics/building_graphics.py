from matplotlib.patches import Polygon
from ..entities.building import BuildingEntity
from matplotlib.axes import Axes

from typing import List


class BuildingPatch:
    """
    A class for plotting a building as a polygon in Matplotlib.

    Creates instance of matplotlib.patches.Polygon, allowing the user to
    directly manipulate polygon properties for the building.

    Parameters:
    -----------
    building : BuildingEntity
        The building object to plot. This object should have a 'vertices' attribute
        which is a list of [x, y] pairs defining the polygon's vertices.
    **kwargs : dict
        Additional keyword arguments are passed directly to the Polygon constructor.
        These can be used to customize the appearance of the polygon (e.g., edgecolor, facecolor).
        Refer to the Matplotlib Polygon documentation for more details on available options.
    """

    def __init__(self, building: BuildingEntity, **kwargs):
        # super().__init__(building.vertices, closed=True, **kwargs)
        self.building = building
        self.building_patch: Polygon = self.create_patch(building.vertices, **kwargs)

    def create_patch(self, vertices: List, **kwargs) -> Polygon:
        """
        Create a polygon patch from the building's vertices.

        This method is called by the matplotlib.axes.Axes.add_patch method
        to add the polygon to the plot.

        Parameters:
        -----------
        building : BuildingEntity
            The building object to plot. This object should have a 'vertices' attribute
            which is a list of [x, y] pairs defining the polygon's vertices.
        """
        building_patch = Polygon(vertices, closed=True, **kwargs)
        return building_patch

    def get_patch(self):
        """
        Get the patchefor the polygon.

        Returns:
        --------
        patch : Polygon
            A matplotlib.patches.Patch objects representing the polygon.
        """
        return self.building_patch

    def set_new_attributes(self, **kwargs):
        """
        Set new attributes for the polygon.

        This method allows the user to update the attributes of the polygon
        without having to create a new BuildingPatch instance.

        Parameters:
        -----------
        **kwargs : dict
            The new attributes to set.
        """
        self.building_patch.set(**kwargs)


class BuildingsPlotter:
    def __init__(self, building_data: dict, edge_color="black", fill_color="darkgray"):
        self.buildings = [
            BuildingEntity([tuple(v[:2]) for v in bld["vertices"]])
            for bld in building_data
        ]
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.building_patches: List[BuildingPatch] = []

    def plot(self, ax: Axes):
        for building in self.buildings:
            building_patch = BuildingPatch(
                building, edgecolor=self.edge_color, facecolor=self.fill_color
            )
            ax.add_patch(building_patch.get_patch())
            self.building_patches.append(building_patch)

    def set_building_attributes(self, **kwargs):
        """
        Set the attributes of the building patches.

        Parameters:
        -----------
        kwargs : dict
            The keyword arguments to pass to the set_new_attributes() method of each BuildingPatch instance.
        """
        for building_patch in self.building_patches:
            building_patch.set_new_attributes(**kwargs)
