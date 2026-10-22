import math
import pytest

from robi.robot import Robot
from robi.geometry import calculate_displacement_fixed_heading
from robi.geometry import shortest_angular_distance


# ========================== Test robot movement, rotation, and angle calculations. ========================== #

def test_move_forward() -> None:
    robi = Robot("Robi")

    robi.move(5)

    assert robi.position.x == pytest.approx(5.0)
    assert robi.position.y == pytest.approx(0.0)
# ======================================================================= #
def test_rotate_and_move() -> None:
    robi = Robot("Robi")

    robi.rotate(90)
    robi.move(3)

    assert robi.position.x == pytest.approx(0.0)
    assert robi.position.y == pytest.approx(3.0)
# ======================================================================= #
def test_angle_normalization() -> None:
    robi = Robot("Robi")

    robi.rotate(450)

    assert robi.position.theta == pytest.approx(math.pi / 2)
# ======================================================================= #
def test_rotate_to_shortest_angle() -> None:
    robi = Robot("Robi")

    robi.rotate(350)
    robi.rotate_to(10)

    assert math.degrees(robi.position.theta) == pytest.approx(10.0)
# ======================================================================= #
def test_shortest_angular_distance() -> None:
    
    current = math.radians(350)
    target = math.radians(10)

    result = shortest_angular_distance(current, target)
    assert math.degrees(result) == pytest.approx(20.0)
# ======================================================================= #
def test_move_to_target() -> None:
    robi = Robot("Robi")

    robi.move_to(3, 4)

    assert robi.position.x == pytest.approx(3.0)
    assert robi.position.y == pytest.approx(4.0)

    expected_angle = math.atan2(4, 3)
    assert robi.position.theta == pytest.approx(expected_angle)
# ======================================================================= #
def test_calculate_displacement() -> None:
    delta_x , delta_y = calculate_displacement_fixed_heading(
                         linear_velocity = 2.0,
                         theta = 0.0,
                         delta_t = 3.0
                        )
    
    assert delta_x == pytest.approx(6.0)
    assert delta_y == pytest.approx(0.0)
# ======================================================================= #
def test_drive_position() -> None:
    
    robi = Robot("Robi")
    robi.drive(linear_velocity = 2.0, angular_velocity = 0.0, delta_t = 3.0)

    assert robi.position.x == pytest.approx(6.0)
    assert robi.position.y == pytest.approx(0.0)
    assert robi.position.theta == pytest.approx(0.0)
# ======================================================================= #
def test_drive_rotation() -> None:
    
    robi= Robot("Robi")
    robi.drive(linear_velocity = 0.0, angular_velocity = 0.5, delta_t = 2.0)
    
    assert robi.position.x == pytest.approx(0.0)
    assert robi.position.y == pytest.approx(0.0)
    assert robi.position.theta == pytest.approx(1.0)
# ======================================================================= #
def test_drive_forward_and_rotate() -> None:
    """Verify that driving updates position and orientation."""

    robi = Robot("robi")
    robi.drive(linear_velocity = 2.0, angular_velocity = 1.0, delta_t = 1.0)
    
    assert robi.position.x == pytest.approx(2.0)
    assert robi.position.y == pytest.approx(0.0)
    assert robi.position.theta == pytest.approx(1.0) 
# ======================================================================= #
def test_drive_wheels_straight() -> None:
    """Verify straight movement with equal wheel speeds."""

    robi = Robot("Robi")

    robi.drive_wheels(
        left_speed=1.0,
        right_speed=1.0,
        wheel_separation=0.5,
        delta_t=2.0
    )

    assert robi.position.x == pytest.approx(2.0)
    assert robi.position.y == pytest.approx(0.0)
    assert robi.position.theta == pytest.approx(0.0)
# ======================================================================= #
def test_drive_wheels_turning() -> None:
    """Verify movement with different wheel speeds."""

    robi = Robot("Robi")

    robi.drive_wheels(
        left_speed=1.0,
        right_speed=2.0,
        wheel_separation=0.5,
        delta_t=1.0
    )

    assert robi.position.x == pytest.approx(1.5)
    assert robi.position.y == pytest.approx(0.0)
    assert robi.position.theta == pytest.approx(2.0)
# ======================================================================= #
