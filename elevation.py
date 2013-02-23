import wpilib

from Globals import *

from RobotSystem import *



class RobotElevation:

    def __init__(self):
        pass

    def Init(self):
        pass


    def OperatorControl(self):
        if testStick.GetRawButton(8):
            robot.elevationMotorUnlimited.Set(testStick.GetY())
        else:
            robot.elevationMotorUnlimited.Set(0)
