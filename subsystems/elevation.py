import wpilib
from core import *
from util.datalog import LoggingPIDController
from util.PIDSources import PIDSourcePot
from util.PIDOutputs import PIDOutputSpeed
from util.CustomControllers import AccelDecelController

class RobotElevation:
    def __init__(self):
        self.pidSource = PIDSourcePot(Robot.elevationPot)
        self.pidOutput = PIDOutputSpeed(Robot.elevationMotor, True)
        self.pid = AccelDecelController(5, self.pidSource, self.pidOutput)
        #self.pid.SetInputRange(prefs.ElevBottomLimit, prefs.ElevTopLimit)
        #self.pid.SetTolerance(0.75)
        #wpilib.SmartDashboard.PutData("elev pid", self.pid)

    def Init(self):
        self.pid.Disable()

    def Stop(self):
        self.pid.Disable()

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
