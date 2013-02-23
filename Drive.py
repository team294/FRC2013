import wpilib
from RobotSystem import *
from util import Subsystem

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

    def ResetEncoders(self):
        robot.rightDriveEncoder.Reset()
        robot.leftDriveEncoder.Reset()

    def Init(self):
        robot.leftTopMotor.SetVoltageRampRate(24.0/0.2)
        robot.leftBottomMotor.SetVoltageRampRate(24.0/0.2)
        robot.rightTopMotor.SetVoltageRampRate(24.0/0.2)
        robot.rightBottomMotor.SetVoltageRampRate(24.0/0.2)
        self.ResetEncoders()

    def ShiftDown(self):
        robot.shifterUp.Set(False)
        robot.shifterDown.Set(True)
        self.shiftTimer.Reset()

    def ShiftUp(self):
        robot.shifterUp.Set(True)
        robot.shifterDown.Set(False)
        self.shiftTimer.Reset()

    def ResetShift(self):
        robot.shifterUp.Set(False)
        robot.shifterDown.Set(False)

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

    def OperatorControl(self):
        if leftStick.GetTrigger():
            self.ShiftDown()
        if rightStick.GetTrigger():
            self.ShiftUp()

        if self.shiftTimer.Get() > .1:
            self.ResetShift()

        lPower = leftStick.GetY()
        rPower = rightStick.GetY()

        self.drive.TankDrive(lPower, rPower)

