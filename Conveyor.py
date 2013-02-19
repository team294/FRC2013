import wpilib

from Globals import *

from RobotSystem import *



class RobotConveyor:

    def __init__(self):
        pass

    def Init(self):
        pass

    def OperatorControl(self): 
        if testStick.GetRawButton(3):
            robot.conveyorMotor.Set(1) 
        else:
            robot.conveyorMotor.Set(0)

