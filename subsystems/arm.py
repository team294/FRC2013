import wpilib
from core import *
import threading

class RobotArm:
    def __init__(self):
        self.armTimer = wpilib.Timer()
        self.armTimer.Start()

        self.armDown = False

        self.armLock = threading.Lock()
        self.resetArmThread = threading.Thread(target=self._ResetArmThread,
                name="ResetArmThread")
        self.resetArmThread.start()

    def Init(self):
        self.armTimer.Reset()

    def Raise(self):
        with self.armLock:
            Robot.armPiston.Set(wpilib.DoubleSolenoid.kForward)
            self.armTimer.Reset()
        self.armDown = False

    def Lower(self):
        with self.armLock:
            Robot.armPiston.Set(wpilib.DoubleSolenoid.kReverse)
            self.armTimer.Reset()
        self.armDown = True

    def IsDown(self):
        return self.armDown

    def IsUp(self):
        return not self.armDown

    def _ResetArmThread(self):
        while 1:
            with self.armLock:
                if self.armTimer.Get() > 0.2:
                    Robot.armPiston.Set(wpilib.DoubleSolenoid.kOff)
            wpilib.Wait(0.1)

