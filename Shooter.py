import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem

class RobotShooter(Subsystem):
    def __init__(self):
        super().__init__()

    def OperatorControl(self):
        if testStick.GetRawButton(10):
            frontVolts = prefs.ShooterFrontTestVolts
            backVolts = prefs.ShooterBackTestVolts
        else:
            frontVolts = 0
            backVolts = 0

        robot.shooterFrontMotor.Set(-frontVolts)
        robot.shooterBackMotor.Set(-backVolts)
