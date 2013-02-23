import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem

class RobotElevation(Subsystem):
    def __init__(self):
        super().__init__()

    def OperatorControl(self):
        if testStick.GetRawButton(8):
            robot.elevationMotorUnlimited.Set(testStick.GetY())
        else:
            robot.elevationMotorUnlimited.Set(0)
