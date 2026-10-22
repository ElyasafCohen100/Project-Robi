
from dataclasses import dataclass

 # ==================== Define the robot's position and orientation in 2D space. ==================== #

@dataclass
class Pose2D:
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0 # Radians
