import math

# ===================== Provide geometric calculations for robot navigation.===================== #

def shortest_angular_distance( current: float,target: float) -> float:
    """ Return the shortest signed angular difference in radians."""
    return (target - current + math.pi) % math.tau - math.pi 

# ================================================================================== #

def calculate_displacement_fixed_heading(linear_velocity: float, theta: float, delta_t: float) -> tuple[float, float]:
    """Calculate 2D displacement over a time step at a fixed heading. """

    if delta_t < 0:
        raise ValueError("Time step cannot be negative")
    
    delta_x = linear_velocity * math.cos(theta)* delta_t
    delta_y = linear_velocity * math.sin(theta)* delta_t
    
    return delta_x, delta_y 

# ================================================================================== #


# =================================================== #
# Odometry  - is the use of data from motion sensors  #
# to estimate the change in an object's position.     #
# =================================================== #

def calculate_displacement_midpoint(center_distance: float, current_theta: float, delta_theta: float) ->tuple[float, float]:
    """Calculate 2D displacement using the midpoint heading approximation."""
    
    midpoint_theta = current_theta + delta_theta / 2
    
    delta_x = center_distance * math.cos(midpoint_theta)
    delta_y = center_distance * math.sin(midpoint_theta)
    
    return delta_x, delta_y # Displacement to add to the robot's current position.