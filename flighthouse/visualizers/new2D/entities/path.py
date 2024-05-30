from typing import List, Tuple

PathElement = List[float]
Path = List[PathElement]


class PathEntity:
    """
    A path is a list of points, where each point is a tuple of (x,y) coordinates.
    path: List[Tuple[float, float]]
    """

    def __init__(self, path: Path):
        self.path = path
