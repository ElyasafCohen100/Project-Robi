import math
import pytest
from robi.robot import Robot


def test_move_forward() -> None:
    robi = Robot("Robi")

    robi.move(5)

    assert robi.position.x == pytest.approx(5.0)
    assert robi.position.y == pytest.approx(0.0)


def test_rotate_and_move() -> None:
    robi = Robot("Robi")

    robi.rotate(90)
    robi.move(3)

    assert robi.position.x == pytest.approx(0.0)
    assert robi.position.y == pytest.approx(3.0)


def test_angle_normalization() -> None:
    robi = Robot("Robi")

    robi.rotate(450)

    assert robi.position.theta == pytest.approx(math.pi / 2)