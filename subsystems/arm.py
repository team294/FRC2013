import wpilib
from core import *
import threading

class RobotArm:
    def __init__(self):
        self.armTimer = wpilib.Timer()
        self.armTimer.Start()

        self.doRaise = False
        self.lowerTimer = wpilib.Timer()

        self.armDown = False
        #self.armDown = True # XXX for LAB TESTING ONLY

        self.mutex = threading.RLock()
        self.armThread = threading.Thread(target=self._ArmThread,
                name="ArmThread")
        self.armThread.start()

    def Init(self):
        self.armTimer.Reset()
        self.ForceElevationLimits()

    def ForceElevationLimits(self):
        with self.mutex:
            if not self.armDown or self.doRaise:
                Robot.elevationMotor.ForceHighLimit(prefs.ElevStartSetpoint)
            else:
                Robot.elevationMotor.ForceHighLimit(None)

    def Raise(self):
        # need to make sure the shooter is out of the way before actuating
        with self.mutex:
            self.doRaise = True
            self.armDown = False
        self.ForceElevationLimits() # enforce tighter limits
        Robot.elevation.GoHome() # raise shooter

    def Lower(self):
        with self.mutex:
            Robot.armPiston.Set(wpilib.DoubleSolenoid.kReverse)
            self.armTimer.Reset()
        # wait a little bit before allowing the shooter to move down
        self.lowerTimer.Start()

    def IsDown(self):
        with self.mutex:
            return self.armDown

    def IsUp(self):
        with self.mutex:
            return not self.armDown

    def _ArmThread(self):
        while 1:
            with self.mutex:
                # handle raise commands
                if self.doRaise:
                    if Robot.elevation.IsArmUpOk():
                        Robot.armPiston.Set(wpilib.DoubleSolenoid.kForward)
                        self.armTimer.Reset()
                        self.doRaise = False

                # handle lower commands
                if self.lowerTimer.Get() > 0.3:
                    self.armDown = True
                    self.lowerTimer.Stop()
                    self.lowerTimer.Reset()
                    self.ForceElevationLimits() # relax limits
                    Robot.elevation.GoHome() # lower shooter

                # pulse latching pneumatics
                if self.armTimer.Get() > 0.2:
                    Robot.armPiston.Set(wpilib.DoubleSolenoid.kOff)
            wpilib.Wait(0.1)

