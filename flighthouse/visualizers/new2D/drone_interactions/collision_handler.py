import numpy as np
from typing import List, Tuple
from pgflow.plotting.entities.drone import DroneEntity


class CollisionManager:
    def __init__(self, drones: List[DroneEntity], collision_distance: float = 0.5):
        # Initialization code for collision management
        self.drones = drones
        self.collision_distance = collision_distance

    def check_collisions(self) -> List[Tuple]:
        """
        Check for drones that are within the threshold distance of each other using NumPy for vectorized calculations.

        Returns:
        --------
        list of tuples
            A list of tuples, each containing the IDs of two drones that are too close to each other.
        """
        positions = np.array([drone.position for drone in self.drones])
        drone_ids = np.array([drone.id for drone in self.drones])

        # Calculate the distance matrix
        dist_matrix = np.sqrt(
            np.sum((positions[:, np.newaxis] - positions[np.newaxis, :]) ** 2, axis=2)
        )

        # Find pairs where the distance is below the threshold
        close_pairs = np.argwhere(dist_matrix < self.collision_distance)

        # Filter out pairs of the same drone and pairs already accounted for
        close_pairs = close_pairs[close_pairs[:, 0] < close_pairs[:, 1]]

        # Convert indices to drone IDs
        close_drones = [(drone_ids[i], drone_ids[j]) for i, j in close_pairs]

        # Convert indices to drone IDs and flatten the array
        colliding_drones = set(drone_ids[np.unique(close_pairs)])

        return colliding_drones


if __name__ == "__main__":

    # Create drones with unique IDs
    drones = [
        DroneEntity(position=(0, 0), goal=(5, 5), radius=2),
        DroneEntity(position=(0, 1), goal=(5, 5), radius=1.5),
        DroneEntity(position=(0, 2), goal=(5, 5), radius=1.5),
    ]

    collision_manager = CollisionManager(drones, collision_distance=1.1)

    print(collision_manager.check_collisions())
