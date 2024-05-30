from typing import List

Point2D = List[float, float]


class WarningCircle:
    # Warning circle entity, contains, position, radius
    def __init__(self, position: Point2D, radius: float):
        self.position = position
        self.radius = radius
