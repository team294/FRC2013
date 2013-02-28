import wpilib
import logging
from core import *
from util.datalog import LoggingPIDController
from util.PIDSources import PIDSourcePot
from util.PIDOutputs import PIDOutputSpeed
from util.CustomControllers import AccelDecelController

class RobotElevation:
    def __init__(self):
        self.pidSource = PIDSourcePot(Robot.elevationPot)
        self.pidOutput = PIDOutputSpeed(Robot.elevationMotor, True)
        self.pid = AccelDecelController(prefs.ElevRampThres, self.pidSource, self.pidOutput)
        #self.pid.SetInputRange(prefs.ElevBottomLimit, prefs.ElevTopLimit)
        #self.pid.SetTolerance(0.75)
        self.pid.SetAbsoluteTolerance(2)
        #wpilib.SmartDashboard.PutData("elev pid", self.pid)

    def Init(self):
        self.pid.Disable()
        self.manual = None

    def Stop(self):
        self.pid.Disable()

    def SetManual(self, value):
        self.manual = value

    def SetOutputs(self):
        mval = 0.0
        if self.manual is not None:
            self.pid.Disable()
            mval = self.manual
        if not self.pid.IsEnabled():
            Robot.elevationMotor.Set(mval)

    def IsArmUpOk(self):
        return self.pidSource.PIDGet() < (prefs.ElevStartSetpoint+2)

    def GoHome(self):
        if Robot.arm.IsUp():
            self.SetStartPosition()
        else:
            self.GoUnderPyramid()

    def GoUnderPyramid(self):
        self.pid.SetSetpoint(prefs.ElevUnderPyramidSetpoint)
        self.pid.Enable()

    def SetHighFrontCenter(self):
        self.pid.SetSetpoint(prefs.ElevHighFrontCenterSetpoint)
        self.pid.Enable()

    def SetHighFrontCorner(self):
        self.pid.SetSetpoint(prefs.ElevHighFrontCornerSetpoint)
        self.pid.Enable()

    def SetHighBackCenter(self):
        self.pid.SetSetpoint(prefs.ElevHighBackCenterSetpoint)
        self.pid.Enable()

    def SetPyramid(self):
        self.pid.SetSetpoint(prefs.ElevPyramidSetpoint)
        self.pid.Enable()

    def SetStartPosition(self):
        self.pid.SetSetpoint(prefs.ElevStartSetpoint)
        self.pid.Enable()

    def OnTarget(self):
        logging.debug("cur: %s setpoint: %s error: %s ontarget: %s",
                self.pidSource.PIDGet(),
                self.pid.GetSetpoint(),
                self.pid.GetError(),
                self.pid.OnTarget())
        return self.pid.OnTarget()

    def TweakDown(self):
        if self.pid.IsEnabled():
            self.pid.SetSetpoint(self.pid.GetSetpoint()-10)
        else:
            self.pid.SetSetpoint(self.pidSource.PIDGet()-10)
            self.pid.Enable()

    def TweakUp(self):
        if self.pid.IsEnabled():
            self.pid.SetSetpoint(self.pid.GetSetpoint()+10)
        else:
            self.pid.SetSetpoint(self.pidSource.PIDGet()+10)
            self.pid.Enable()
