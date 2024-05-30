from numpy.typing import NDArray
from numpy import float64

Point2D = NDArray[float64]


class ArrowEntity:
    # class with arrow start and end points
    def __init__(self, start: Point2D, end: Point2D):
        self.start = start
        self.end = end
