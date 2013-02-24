import wpilib
from core import *

class RobotFeeder:
    def __init__(self):
        pass

    def Init(self):
        self.running = False

    def SetOutputs(self):
        if self.running:
            Robot.feederMotor.Set(1)
        else:
            Robot.feederMotor.Set(0)

    def Run(self):
        self.running = True

    def Stop(self):
        self.running = False

