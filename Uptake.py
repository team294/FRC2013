import wpilib

from Globals import *

from RobotSystem import *



class RobotUptake:

    def __init__(self):
        pass

    def Init(self):
        pass


    def OperatorControl(self):
        if testStick.GetRawButton(3):
            robot.dumbyMotorUnlimited.Set(testStick.GetY())
        else:
            robot.dumbyMotorUnlimited.Set(0)


