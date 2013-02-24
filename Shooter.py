import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem

class RobotShooter(Subsystem):
    def __init__(self):
        super().__init__()

    def Init(self):
        self.frontVolts = 0
        self.backVolts = 0

    def SetOutputs(self):
        robot.shooterFrontMotor.Set(-self.frontVolts)
        robot.shooterBackMotor.Set(-self.backVolts)

    def SetTestSpeed(self):
        self.frontVolts = prefs.ShooterFrontTestVolts
        self.backVolts = prefs.ShooterBackTestVolts

    def Stop(self):
        self.frontVolts = 0
        self.backVolts = 0

