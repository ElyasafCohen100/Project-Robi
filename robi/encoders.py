"""Convert wheel encoder measurements into travel distances."""

import math

# ================================================================================== #

def calculate_wheel_distance(pulses: int, pulses_per_revolution: int, wheel_diameter: float) -> float:
    """Calculate wheel travel distance from signed encoder pulses."""

    if pulses_per_revolution <= 0:
        raise ValueError("Pulses per revolution must be positive")

    if wheel_diameter <= 0:
        raise ValueError("Wheel diameter must be positive")
    
    rotations = pulses / pulses_per_revolution
    
    return rotations * math.pi * wheel_diameter

# ================================================================================== #

