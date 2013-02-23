import wpilib

from Globals import *
from RobotSystem import *

class RobotArm:

    def __init__(self):
        self.armTimer = wpilib.Timer()
        self.armTimer.Start()

    def Init(self):
        pass

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

