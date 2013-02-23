import wpilib

from Globals import *

from RobotSystem import *



class RobotConveyor:

    def __init__(self):
        pass

    def Init(self):
        pass

    def OperatorControl(self):
        pass
        if testStick.GetRawButton(2):
            robot.conveyorMotor.Set(1)
            pass
        else:
            robot.conveyorMotor.Set(0)
            pass


