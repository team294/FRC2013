import wpilib
from Globals import *
from RobotSystem import *
from util import Subsystem
from util.datalog import LoggingPIDController
from util.PIDSources import PIDSourcePot
from util.PIDOutputs import PIDOutputSpeed

class RobotUptake(Subsystem):
    def __init__(self):
        super().__init__()
        self.pidSource = PIDSourcePot(robot.uptakePot)
        self.pidOutput = PIDOutputSpeed(robot.uptakeMotor, True)
        self.pid = wpilib.PIDController(prefs.UptakeP, prefs.UptakeI, prefs.UptakeD,
                self.pidSource, self.pidOutput)#, port=8880)
        wpilib.SmartDashboard.PutData("uptake pid", self.pid)

    def Init(self):
        self.pid.Disable()

    def PositionForIntake(self):
        self.pid.SetPID(prefs.UptakeIntakeP, prefs.UptakeIntakeI, prefs.UptakeIntakeD)
        r = prefs.UptakeIntakeOutputRange
        self.pid.SetOutputRange(-r, r)
        self.pid.SetSetpoint(prefs.UptakeIntakeSetpoint)
        self.pid.Enable()

    def PositionForArming(self):
        self.pid.SetPID(prefs.UptakeArmP, prefs.UptakeArmI, prefs.UptakeArmD)
        r = prefs.UptakeArmOutputRange
        self.pid.SetOutputRange(-r, r)
        self.pid.SetSetpoint(prefs.UptakeArmSetpoint)
        self.pid.Enable()

    def StartFiring(self):
        self.pid.SetPID(prefs.UptakeFireP, prefs.UptakeFireI, prefs.UptakeFireD)
        r = prefs.UptakeFireOutputRange
        self.pid.SetOutputRange(-r, r)
        self.pid.SetSetpoint(prefs.UptakeFireSetpoint)
        self.pid.Enable()

    def Stop(self):
        self.pid.Disable()

    def InIntakePosition(self):
        return robot.uptakePot.GetAverageValue() > (prefs.UptakeIntakeSetpoint - 10)
