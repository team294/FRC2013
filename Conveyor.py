import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem

class RobotConveyor(Subsystem):
    def __init__(self):
        super().__init__()

    def Init(self):
        self.running = False

    def SetOutputs(self):
        if self.running:
            robot.conveyorMotor.Set(1)
        else:
            robot.conveyorMotor.Set(0)

    def OperatorControl(self):
        # clicking the button stops/starts
        if testStick.GetRawButton(2) and not robot.lastTestButtons[2]:
            self.running = not self.running

        self.SetOutputs()

