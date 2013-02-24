import wpilib
import logging
from core import *
from util.datalog import *
from util.Filters import *

class RobotShooter:
    def __init__(self):
        self.mutex = threading.RLock()

        # Configure motors
        Robot.shooterFrontMotor.SetVoltageRampRate(24.0/0.2)
        Robot.shooterBackMotor.SetVoltageRampRate(24.0/0.2)

        # Initialize sensors
        Robot.backShooterCounter.SetMaxPeriod(0.5)
        Robot.frontShooterCounter.SetMaxPeriod(0.5)
        Robot.backShooterCounter.Start()
        Robot.frontShooterCounter.Start()

        # Timers
        self.armedTime = wpilib.Timer()
        self.fireTime = wpilib.Timer()
        self.lastImageTime = wpilib.Timer()
        self.lastImageTime.Start()

        # wheel PIDs
        #self.frontShooterCounterFiltered = FlatAverageFilter(robot.frontShooterCounter.GetPeriod, 8, 0.05/8.0)
        #self.frontSpeedControl = SpeedPIDController(prefs.ShooterFrontP, prefs.ShooterFrontI, prefs.ShooterFrontD, self.frontShooterCounterFiltered.GetAverage, robot.frontShooterMotor, frontShooterFeedForward, period=0.05, port=8885)
        #self.frontSpeedControl.SetInputRange(0.0, 40.0)
        #self.frontSpeedControl.SetTolerance(5.0)
        #wpilib.SmartDashboard.PutData("speed front", self.frontSpeedControl)

        #self.backShooterCounterFiltered = FlatAverageFilter(roback.backShooterCounter.GetPeriod, 8, 0.05/8.0)
        #self.backSpeedControl = SpeedPIDController(prefs.ShooterBackP, prefs.ShooterBackI, prefs.ShooterBackD, self.backShooterCounterFiltered.GetAverage, roback.backShooterMotor, backShooterFeedForward, period=0.05, port=8886)
        #self.backSpeedControl.SetInputRange(0.0, 40.0)
        #self.backSpeedControl.SetTolerance(5.0)
        #wpilib.SmartDashboard.PutData("speed back", self.backSpeedControl)

        # shooter speed data logger (for testing purposes)
        self.shooterspeed = 0.0
        self.shooterspeeddata_struct = struct.Struct("<ddd")
        self.shooterspeed_logger = DataLogger(self.GetShooterSpeedData, 0.05, 8900)
        #self.shooterspeed_logger.start()

    def Init(self):
        self.frontVolts = 0
        self.backVolts = 0
        self.armed = False
        self.firing = False

    def GetShooterSpeedData(self):
        avg = self.backShooterCounterFiltered.GetAverage()
        if avg == 0:
            return self.shooterspeeddata_struct.pack(self.shooterspeed, 1.0/robot.backShooterCounter.GetPeriod(), 0.0)
        else:
            return self.shooterspeeddata_struct.pack(self.shooterspeed, 1.0/robot.backShooterCounter.GetPeriod(), 1.0/avg)

    def SetOutputs(self):
        Robot.shooterFrontMotor.Set(-self.frontVolts)
        Robot.shooterBackMotor.Set(-self.backVolts)

    def SetTestSpeed(self):
        self.frontVolts = prefs.ShooterFrontTestVolts
        self.backVolts = prefs.ShooterBackTestVolts

    def Stop(self):
        self.frontVolts = 0
        self.backVolts = 0

    def Arm(self):
        with self.mutex:
            if self.armed:
                return
        self.armedTime.Reset()
        self.armedTime.Start()
        logging.info("Shooter: Arming")
        with self.mutex:
            self.armed = True

    def StopArm(self):
        with self.mutex:
            if not self.armed:
                return
        self.armedTime.Stop()
        self.armedTime.Reset()
        logging.info("Shooter: Disarming")
        with self.mutex:
            self.armed = False

    def Fire(self):
        # Don't allow firing unless we're armed and on target
        with self.mutex:
            if not self.armed:# or not self.OnTarget():
                return
            if self.firing:
                return
        self.fireTime.Reset()
        self.fireTime.Start()
        with self.mutex:
            self.firing = True

    def StopFire(self):
        with self.mutex:
            if not self.firing:
                return
        self.fireTime.Stop()
        self.fireTime.Reset()
        with self.mutex:
            self.firing = False

