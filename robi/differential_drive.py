
 
def calculate_linear_velocity(left_speed: float, right_speed: float) -> float: 
    """Calculate the robot's center linear velocity in m/s"""
    return (left_speed + right_speed) / 2

# ================================================================================== #

def calculate_angular_velocity(left_speed: float, right_speed: float, wheel_separation: float) -> float:
    """angular velocity in Rad/s"""
   
    if wheel_separation <= 0:
        raise ValueError("Wheel base must be positive")
      
    return (right_speed - left_speed) / wheel_separation    
    
# ================================================================================== #
   
   
   
# =================================================== #
# Odometry  - is the use of data from motion sensors  #
# to estimate the change in an object's position.     #
# =================================================== #
 
    
# Δs - distance(by wheels) 
def calculate_center_distance(left_distance: float, right_distance: float) -> float:
    """Calculate the distance traveled by the robot's center from wheel travel distances."""
    return (left_distance + right_distance) / 2

# ================================================================================== #

# Δθ - theta(by wheels) 
def calculate_heading_change(left_distance: float, right_distance:float, wheel_separation:float) ->None:
    """Calculate the robot's heading change, from wheel travel distances, in radians."""
    
    if wheel_separation <= 0:
        raise ValueError("Wheel separetion must be positive")
    
    return(right_distance-left_distance) /wheel_separation

# ================================================================================== #