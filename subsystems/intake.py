import wpilib
from core import *

class RobotIntake:
    def __init__(self):
        pass

    def Init(self):
        self.running = False

    def SetOutputs(self):
        if self.running:
            Robot.intakeMotor.Set(1)
        else:
            Robot.intakeMotor.Set(0)

    def Run(self):
        self.running = True

    def Stop(self):
        self.running = False

