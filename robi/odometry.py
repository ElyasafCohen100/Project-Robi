"""Estimate a robot's pose from measured wheel travel distances."""
import math

from robi.pose_2d import Pose2D
from robi.geometry import calculate_displacement_midpoint
from robi.differential_drive import(calculate_center_distance, calculate_heading_change,)



class Odometry:
    """Track the robot's estimated position and heading."""

    def __init__(self) -> None:
        """Initialize the robot's estimated pose at the origin."""
        self.pose = Pose2D()

# ================================================================================== #

    def update(self, left_distance: float, right_distance: float, wheel_separation: float) -> None:
        """Update the estimated pose using measured wheel travel distances."""
                     
        delta_s = calculate_center_distance(left_distance, right_distance)
        delta_theta = calculate_heading_change(left_distance, right_distance, wheel_separation)
        delta_x, delta_y = calculate_displacement_midpoint(delta_s, self.pose.theta, delta_theta)
        
        self.pose.x += delta_x
        self.pose.y += delta_y
        self.pose.theta = (self.pose.theta + delta_theta) % math.tau
        
# ================================================================================== #

