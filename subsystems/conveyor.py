import wpilib
from core import *

class RobotConveyor:
    def __init__(self):
        pass

    def Init(self):
        self.running = False

    def SetOutputs(self):
        if self.running:
            Robot.conveyorMotor.Set(1)
        else:
            Robot.conveyorMotor.Set(0)

    def Run(self):
        self.running = True

    def Stop(self):
        self.running = False

