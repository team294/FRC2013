import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem

class RobotArm(Subsystem):
    def __init__(self):
        super().__init__()
        self.armTimer = wpilib.Timer()
        self.armTimer.Start()

    def Init(self):
        self.armTimer.Reset()

    def Raise(self):
        robot.armUp.Set(True)
        robot.armDown.Set(False)
        self.armTimer.Reset()

    def Lower(self):
        robot.armUp.Set(False)
        robot.armDown.Set(True)
        self.armTimer.Reset()

    def Reset(self):
        robot.armUp.Set(False)
        robot.armDown.Set(False)

    def OperatorControl(self):
        if testStick.GetRawButton(6):
            self.Raise()

        if testStick.GetRawButton(7):
            self.Lower()

        if self.armTimer.Get() > .1:
            self.Reset()

