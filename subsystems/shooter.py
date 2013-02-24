import wpilib
from core import *

class RobotShooter:
    def __init__(self):
        pass

    def Init(self):
        self.frontVolts = 0
        self.backVolts = 0

    def SetOutputs(self):
        Robot.shooterFrontMotor.Set(-self.frontVolts)
        Robot.shooterBackMotor.Set(-self.backVolts)

    def SetTestSpeed(self):
        self.frontVolts = prefs.ShooterFrontTestVolts
        self.backVolts = prefs.ShooterBackTestVolts

    def Stop(self):
        self.frontVolts = 0
        self.backVolts = 0
