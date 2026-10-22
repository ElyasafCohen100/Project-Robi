
import pytest

from robi.differential_drive import (
    calculate_linear_velocity, 
    calculate_angular_velocity
    )

 
# ================================================= #
def test_calculate_linear_velocity() -> None:
    
    result = calculate_linear_velocity(1.0, 2.0)
    assert result == pytest.approx(1.5)
    
# ================================================= #
def test_calculate_angular_velocity() -> None:
    result = calculate_angular_velocity(1.0, 2.0, 0.5)
    
    assert result == pytest.approx(2.0)
    
# ================================================= #
def test_invalid_wheel_base() -> None:
     with pytest.raises(ValueError):
        calculate_angular_velocity(1.0, 2.0, 0.0)
        
# ================================================= #