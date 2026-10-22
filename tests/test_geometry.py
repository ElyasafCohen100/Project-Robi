import math
import pytest

from robi.geometry import (
    shortest_angular_distance,
    calculate_displacement_fixed_heading,
)

"""Test the geometry calculation functions."""

# ======================================================================= #
def test_shortest_angular_distance() -> None:
    """Check that the shortest turn is calculated correctly."""
    current = math.radians(350)
    target = math.radians(10)

    result = shortest_angular_distance(current, target)

    assert math.degrees(result) == pytest.approx(20.0)
    
# ======================================================================= #
def test_calculate_displacement_fixed_heading() -> None:
    """Check the movement calculated from speed, direction, and time."""
    delta_x, delta_y = calculate_displacement_fixed_heading(
        linear_velocity=2.0,
        theta=0.0,
        delta_t=3.0
    )

    assert delta_x == pytest.approx(6.0)
    assert delta_y == pytest.approx(0.0)
    
# ======================================================================= #
