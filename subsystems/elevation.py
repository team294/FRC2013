import wpilib
from core import *
from util.datalog import LoggingPIDController
from util.PIDSources import PIDSourcePot
from util.PIDOutputs import PIDOutputSpeed

class RobotElevation:
    def __init__(self):
        self.pidSource = PIDSourcePot(Robot.elevationPot)
        #self.pidOutput = PIDOutputSpeed(Robot.elevationMotor, True)
        #self.pid = wpilib.PIDController(prefs.ElevP, prefs.ElevI, prefs.ElevD,
        #        self.pidSource, self.pidOutput)#, port=8888)
        #self.pid.SetInputRange(prefs.ElevBottomLimit, prefs.ElevTopLimit)
        #self.pid.SetTolerance(0.75)
        #wpilib.SmartDashboard.PutData("elev pid", self.pid)

    def Init(self):
        #self.pid.Disable()
        pass

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
            self.pid.SetSetpoint(self.pid.GetSetpoint()-10)
            self.pid.Enable()

    def TweakUp(self):
        pass
