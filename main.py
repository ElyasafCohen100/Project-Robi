
import math
from robi.robot import Robot


def main() -> None:
    robi = Robot("Robi")

    robi.move(5)
    robi.rotate(90)
    robi.move(30)

    print(f"X: {robi.position.x:.2f}")
    print(f"Y: {robi.position.y:.2f}")
    print(f"Theta: {math.degrees(robi.position.theta):.2f}°")
    

if __name__ == "__main__":
    main()
