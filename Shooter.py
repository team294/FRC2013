import wpilib

from Globals import *

from RobotSystem import *



class RobotShooter:

    def __init__(self):
        pass

    def Init(self):
        pass
    
    
    def OperatorControl(self):
        if testStick.GetRawButton(10):
            robot.shooterFrontMotor.Set(testStick.GetY())
            robot.shooterBackMotor.Set(testStick.GetY())
        else:
            robot.shooterFrontMotor.Set(0)   
            robot.shooterBackMotor.Set(0)
