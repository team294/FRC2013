import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem

class RobotShooter(Subsystem):
    def __init__(self):
        super().__init__()

    def OperatorControl(self):
        if testStick.GetRawButton(10):
            robot.shooterFrontMotor.Set(12*testStick.GetY())
            robot.shooterBackMotor.Set(12*testStick.GetY())
        else:
            robot.shooterFrontMotor.Set(0)
            robot.shooterBackMotor.Set(0)
