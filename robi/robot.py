
"""Define the robot and its movement behavior."""

import math

from .pose_2d import Pose2D
from .geometry import shortest_angular_distance, calculate_displacement_fixed_heading
from .differential_drive import calculate_angular_velocity, calculate_linear_velocity


class Robot:
    """Represent a robot with a position, direction, and battery."""

# ==================================================================================== #

    def __init__(self, name: str):
        """Create a robot with a name, starting position, and full battery."""
        self.name = name
        self.position = Pose2D()
        self.battery_level = 100.0
        
# ==================================================================================== #

    # Example: Move 5 meters forward
    def move(self, distance: float) -> None:
        """Move the robot by a given distance in its current direction."""
        self.position.x += distance * math.cos(self.position.theta)
        self.position.y += distance * math.sin(self.position.theta)

# ==================================================================================== #

    # Example: Turn 90 degrees left
    def rotate(self, angle: float) -> None:
        """Rotate the robot by a relative angle in degrees."""
        self.position.theta = (self.position.theta + math.radians(angle)) % math.tau # from 0 to 2π  

# ==================================================================================== #

    # Example: Move to (3, 4).
    def move_to(self, target_x: float, target_y: float) -> None:
        """Turn toward a target point and move directly to it."""

        delta_x = target_x - self.position.x
        delta_y = target_y - self.position.y    

        distance = math.hypot(delta_x, delta_y) # Calculate the "Yeter"

        if distance == 0:
            return

        # atan2(y,x)
        target_angle = math.degrees(math.atan2(delta_y, delta_x))  # Calculate the theta for target.

        self.rotate_to(target_angle)
        self.move(distance)

# ==================================================================================== #

    #  Example: Face North (90 degrees)
    def rotate_to(self, target_angle: float) -> None:
        """Face a target direction using the shortest turn."""

        target = math.radians(target_angle)
        angle_difference = shortest_angular_distance(self.position.theta,target)

        # Keep the direction between 0 and 2*pi radians.
        self.position.theta += angle_difference
        self.position.theta %= math.tau

# ==================================================================================== #

    def drive(self, linear_velocity: float, angular_velocity: float, delta_t: float) -> None:
        """Update the robot's position and orientation over time."""

        delta_x, delta_y = calculate_displacement_fixed_heading(
            linear_velocity,
            self.position.theta,
            delta_t
        )

        self.position.x += delta_x
        self.position.y += delta_y
        
        self.position.theta += angular_velocity * delta_t # (Δθ = ω ⋅ Δt)
        self.position.theta %= math.tau # from 0 to 2π  

# ==================================================================================== #

    def drive_wheels(self, left_speed: float, right_speed:float, wheel_separation: float, delta_t: float) -> None:
        """Drive the robot using differential wheel speeds."""
            
        linear_velocity = calculate_linear_velocity(
            left_speed, right_speed
        )
    
        angular_velocity = calculate_angular_velocity (
            left_speed, right_speed, wheel_separation
        )
        
        self.drive(linear_velocity, angular_velocity, delta_t)
        
# ==================================================================================== #
