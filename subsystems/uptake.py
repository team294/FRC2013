import wpilib
from core import *
import logging
from util.datalog import LoggingPIDController
from util.PIDSources import PIDSourcePot
from util.PIDOutputs import PIDOutputSpeed

class RobotUptake:
    def __init__(self):
        self.pidSource = PIDSourcePot(Robot.uptakePot)
        self.pidOutput = PIDOutputSpeed(Robot.uptakeMotor, True)
        self.pid = wpilib.PIDController(prefs.UptakeP, prefs.UptakeI, prefs.UptakeD,
                self.pidSource, self.pidOutput)#, port=8880)
        wpilib.SmartDashboard.PutData("uptake pid", self.pid)
        self.manual = None
        self.firing = False

    def Init(self):
        self.pid.Disable()

    def SetManual(self, value):
        self.manual = value

    def SetOutputs(self):
        mval = 0.0
        if self.firing:
            self.pid.Disable()
            if self.pidSource.PIDGet() < prefs.UptakeFireSetpoint:
                # hit the top
                mval = 0.0
            elif self.pidSource.PIDGet() < (prefs.UptakeArmSetpoint+20):
                # feed the feeder
                mval = prefs.UptakeFireOutputRange
            else:
                # if below the arm setpoint, drive up at "full" speed
                mval = 0.4
            logging.debug("source=%s, mval=%s", self.pidSource.PIDGet(), mval)
        if self.manual is not None:
            self.pid.Disable()
            mval = self.manual
        if not self.pid.IsEnabled():
            Robot.uptakeMotor.Set(mval)

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
        self.firing = True
        #self.pid.Disable()
        #self.pid.SetPID(prefs.UptakeFireP, prefs.UptakeFireI, prefs.UptakeFireD)
        #r = prefs.UptakeFireOutputRange
        #self.pid.SetOutputRange(-r, r)
        #self.pid.SetSetpoint(prefs.UptakeFireSetpoint)
        #self.pid.Enable()

    def StopFiring(self):
        self.firing = False

    def Stop(self):
        self.pid.Disable()

    def InIntakePosition(self):
        return Robot.uptakePot.GetAverageValue() > (prefs.UptakeIntakeSetpoint - 10)

