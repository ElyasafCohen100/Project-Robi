"""Test odometry pose estimation from wheel travel distances."""

import math
import pytest

from robi.odometry import Odometry

# ================================================================================== #

def test_odometry_straight_motion()->None:
     """Verify that equal wheel distances produce straight motion."""

     odometry = Odometry()
     odometry.update(left_distance = 1.0, right_distance = 1.0, wheel_separation = 0.5)
    
     assert odometry.pose.x == pytest.approx(1.0)
     assert odometry.pose.y == pytest.approx(0.0)
     assert odometry.pose.theta == pytest.approx(0,0)
     
# ================================================================================== #

def test_odometry_rotation_in_place()-> None:
    """Verify that opposite wheel distances rotate the robot in place."""
          
    odometry = Odometry()
    odometry.update(left_distance = -0.5, right_distance = 0.5, wheel_separation = 0.5)
    
    assert odometry.pose.x == pytest.approx(0.0)
    assert odometry.pose.y == pytest.approx(0.0)
    assert odometry.pose.theta == pytest.approx(2.0)

# ================================================================================== #

def test_odometry_curved_motion() -> None:
    """Verify pose estimation during curved motion."""
   
    odometry = Odometry()
    odometry.update(left_distance = 0.5, right_distance=1.0, wheel_separation=0.5)

    assert odometry.pose.x == pytest.approx(0.75 * math.cos(0.5))
    assert odometry.pose.y == pytest.approx(0.75 * math.sin(0.5))
    assert odometry.pose.theta == pytest.approx(1.0)
        
# ================================================================================== #
    
def test_odometry_multiple_updates() -> None:
    """Verify that consecutive updates accumulate robot movement."""
    
    odometry = Odometry()
    odometry.update(left_distance = 1.0, right_distance = 1.0, wheel_separation = 0.5)
    odometry.update(left_distance = 1.0, right_distance = 1.0, wheel_separation = 0.5)

    assert odometry.pose.x == pytest.approx(2.0)
    assert odometry.pose.y == pytest.approx(0.0)
    assert odometry.pose.theta == pytest.approx(0.0)

# ================================================================================== #

def test_odometry_rotation_then_forward() -> None:
    """Verify that forward motion uses the heading from a previous update."""

    odometry = Odometry()
    quarter_turn_distance = math.pi / 8
    
    odometry.update(left_distance = -quarter_turn_distance, right_distance = quarter_turn_distance, wheel_separation = 0.5)
    odometry.update(left_distance = 1.0, right_distance = 1.0, wheel_separation = 0.5)

    assert odometry.pose.x == pytest.approx(0.0)
    assert odometry.pose.y == pytest.approx(1.0)

# ================================================================================== #

