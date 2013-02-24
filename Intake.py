import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem

class RobotIntake(Subsystem):
    def __init__(self):
        super().__init__()

    def Init(self):
        self.running = False

    def SetOutputs(self):
        if self.running:
            robot.intakeMotor.Set(1)
        else:
            robot.intakeMotor.Set(0)

    def Run(self):
        self.running = True

    def Stop(self):
        self.running = False

