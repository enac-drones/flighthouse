from typing import List

Vertex2D = List[float]
VertexList = List[Vertex2D]


class BuildingEntity:
    # building entity with a list of vertices
    def __init__(self, vertices: VertexList):
        self.vertices = vertices

    def __repr__(self):
        return f"Building({self.vertices})"
