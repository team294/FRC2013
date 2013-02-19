import wpilib

from Globals import *

from RobotSystem import *



class RobotIntake:

    def __init__(self):
        pass
    
    def Init(self):
        pass
    
    def OperatorControl(self):
        if testStick.GetRawButton(2):
            robot.intakeMotor.Set(1)
        else:
            robot.intakeMotor.Set(0)
        
