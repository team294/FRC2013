import wpilib

from Globals import *

from RobotSystem import *



class RobotFeeder:

    def __init__(self):
        pass

    def Init(self):
        pass


    def OperatorControl(self):
        if testStick.GetRawButton(5):
            robot.feederMotor.Set(1)
        else:
            robot.feederMotor.Set(0)

