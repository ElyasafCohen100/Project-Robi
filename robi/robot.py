import math
from .pose_2d import Pose2D


class Robot:
    def __init__(self, name: str):
        self.name = name
        self.position = Pose2D()
        self.battery_level = 100.0
        
        
    def move(self,distance: float) -> None:
        self.position.x += distance*math.cos(self.position.theta)
        self.position.y += distance*math.sin(self.position.theta)


    def rotate(self, angle: float) -> None:
       self.position.theta = (self.position.theta + math.radians(angle)) % math.tau 

