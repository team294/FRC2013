import wpilib
from core import *
import threading

class RobotDrive:
    def __init__(self):
        self.drive = wpilib.RobotDrive(Robot.leftMotor, Robot.rightMotor)
        Robot.leftDriveEncoder.Start()
        Robot.rightDriveEncoder.Start()
        #Robot.leftDriveEncoder.SetDistancePerPulse(1.0/prefs.DriveTicksPerInch)
        #Robot.rightDriveEncoder.SetDistancePerPulse(1.0/prefs.DriveTicksPerInch)
        self.shiftTimer = wpilib.Timer()
        self.shiftTimer.Start()

        self.shiftLock = threading.Lock()
        self.resetShiftThread = threading.Thread(target=self._ResetShiftThread,
                name="ResetShiftThread")
        self.resetShiftThread.start()

    def ResetEncoders(self):
        Robot.rightDriveEncoder.Reset()
        Robot.leftDriveEncoder.Reset()

    def Init(self):
        Robot.leftTopMotor.SetVoltageRampRate(24.0/0.2)
        Robot.leftBottomMotor.SetVoltageRampRate(24.0/0.2)
        Robot.rightTopMotor.SetVoltageRampRate(24.0/0.2)
        Robot.rightBottomMotor.SetVoltageRampRate(24.0/0.2)
        self.ResetEncoders()

    def _ResetShiftThread(self):
        while 1:
            with self.shiftLock:
                if self.shiftTimer.Get() > 0.2:
                    Robot.shifterPiston.Set(wpilib.DoubleSolenoid.kOff)
            wpilib.Wait(0.1)

    def ShiftDown(self):
        with self.shiftLock:
            Robot.shifterPiston.Set(wpilib.DoubleSolenoid.kReverse)
            self.shiftTimer.Reset()

    def ShiftUp(self):
        with self.shiftLock:
            Robot.shifterPiston.Set(wpilib.DoubleSolenoid.kForward)
            self.shiftTimer.Reset()

    def AutoDrive(self, speed):
        leftValue = -Robot.leftDriveEncoder.Get()*250.0/360.0 # real base
        rightValue = -Robot.rightDriveEncoder.Get()

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

