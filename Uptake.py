import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem

class RobotUptake(Subsystem):
    def __init__(self):
        super().__init__()

    def OperatorControl(self):
        if testStick.GetRawButton(3):
            robot.uptakeMotorUnlimited.Set(testStick.GetY()/2.0)
        else:
            robot.uptakeMotorUnlimited.Set(0)

