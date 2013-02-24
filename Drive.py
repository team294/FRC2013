import wpilib
from RobotSystem import *
from util import Subsystem
import threading

class RobotDrive(Subsystem):
    def __init__(self):
        super().__init__()
        self.drive = wpilib.RobotDrive(robot.leftMotor, robot.rightMotor)
        robot.leftDriveEncoder.Start()
        robot.rightDriveEncoder.Start()
        #robot.leftDriveEncoder.SetDistancePerPulse(1.0/prefs.DriveTicksPerInch)
        #robot.rightDriveEncoder.SetDistancePerPulse(1.0/prefs.DriveTicksPerInch)
        self.shiftTimer = wpilib.Timer()
        self.shiftTimer.Start()

        self.shiftLock = threading.Lock()
        self.resetShiftThread = threading.Thread(target=self._ResetShiftThread,
                name="ResetShiftThread")
        self.resetShiftThread.start()

    def ResetEncoders(self):
        robot.rightDriveEncoder.Reset()
        robot.leftDriveEncoder.Reset()

    def Init(self):
        robot.leftTopMotor.SetVoltageRampRate(24.0/0.2)
        robot.leftBottomMotor.SetVoltageRampRate(24.0/0.2)
        robot.rightTopMotor.SetVoltageRampRate(24.0/0.2)
        robot.rightBottomMotor.SetVoltageRampRate(24.0/0.2)
        self.ResetEncoders()

    def _ResetShiftThread(self):
        while 1:
            with self.shiftLock:
                if self.shiftTimer.Get() > 0.2:
                    robot.shifterUp.Set(False)
                    robot.shifterDown.Set(False)
            wpilib.Wait(0.1)

    def ShiftDown(self):
        with self.shiftLock:
            robot.shifterUp.Set(False)
            robot.shifterDown.Set(True)
            self.shiftTimer.Reset()

    def ShiftUp(self):
        with self.shiftLock:
            robot.shifterUp.Set(True)
            robot.shifterDown.Set(False)
            self.shiftTimer.Reset()

    def AutoDrive(self, speed):
        leftValue = -robot.leftDriveEncoder.Get()*250.0/360.0 # real base
        rightValue = -robot.rightDriveEncoder.Get()

        leftSpeed = speed
        rightSpeed = speed
        if leftValue > rightValue:
            leftSpeed -= (leftValue-rightValue)/24.0
        elif leftValue < rightValue:
            rightSpeed -= (rightValue-leftValue)/24.0

        print("lenc: %s renc: %s lout: %s rout: %s" % (leftValue, rightValue, leftSpeed, rightSpeed))
        self.drive.TankDrive(leftSpeed, rightSpeed)

    def TankDrive(self, lPower, rPower):
        self.drive.TankDrive(lPower, rPower)

