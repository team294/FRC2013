import wpilib
from core import *
##from ImageProcessing import ImageProcessor

class Autonomous:
    CENTER = 0
    LEFT = 1
    RIGHT = 2
    positionName = {CENTER: "center", LEFT: "left", RIGHT: "right"}
    autoModes = [
        ("do nothing", "do nothing"),
        ("Front 2", "shoot 2 from front"), #1
        ("Front 4", "shoot 2, pickup/shoot 2 from front"),
        ("Back 3", "shoot 3 from back"),
        ("TEST 4ft", "TEST MODE 4 ft straight drive"),
        ]

    def __init__(self):
        self.autoMode = 1
        self.startPosition = self.CENTER
        self.startDelay = 0.0

    def DisplayMode(self):
        dselcd = wpilib.DriverStationLCD.GetInstance()
        dselcd.PrintLine(wpilib.DriverStationLCD.kUser_Line1,
                         "A%d: %s" % (self.autoMode, self.autoModes[self.autoMode][0]))
        dselcd.PrintLine(wpilib.DriverStationLCD.kUser_Line2,
                         "Pos: %s" % (self.positionName[self.startPosition]))
        dselcd.PrintLine(wpilib.DriverStationLCD.kUser_Line3,
                         "Delay: %2.1f" % self.startDelay)
        print("Autonomous %s Position %s Delay %2.1f" %
                (self.autoModes[self.autoMode][1],
                 self.positionName[self.startPosition],
                 self.startDelay))
        dselcd.UpdateLCD()

    def ModeSelection(self):
        display = False

        # mode setting
        if OI.leftStick.GetTrigger() and not OI.lastLeftButtons[1]:
            self.autoMode -= 1
            if self.autoMode < 0:
                self.autoMode = 0
            else:
                display = True
        elif OI.rightStick.GetTrigger() and not OI.lastRightButtons[1]:
            self.autoMode += 1
            if self.autoMode >= len(self.autoModes):
                self.autoMode = len(self.autoModes)-1
            else:
                display = True

        # start position setting
        if OI.leftStick.GetRawButton(4):
            if self.startPosition != self.LEFT:
                self.startPosition = self.LEFT
                display = True
        if OI.leftStick.GetRawButton(3):
            if self.startPosition != self.CENTER:
                self.startPosition = self.CENTER
                display = True
        if OI.leftStick.GetRawButton(5):
            if self.startPosition != self.RIGHT:
                self.startPosition = self.RIGHT
                display = True

        # start delay setting
        if OI.rightStick.GetRawButton(4) and not OI.lastRightButtons[4]:
            self.startDelay -= 0.1
            if self.startDelay < 0:
                self.startDelay = 0
            else:
                display = True
        if OI.rightStick.GetRawButton(5) and not OI.lastRightButtons[5]:
            self.startDelay += 0.1
            if self.startDelay > 10:
                self.startDelay = 10
            else:
                display = True

        if display:
            self.DisplayMode()
            

    def Run(self):
        wpilib.GetWatchdog().SetExpiration(1.0)
        wpilib.GetWatchdog().SetEnabled(True)
        time = wpilib.Timer()
        deltaTime = wpilib.Timer()

        time.Start()
        deltaTime.Start()

        prevState = -1
        state = 0

        while wpilib.IsAutonomous() and wpilib.IsEnabled():
            wpilib.GetWatchdog().Feed()
            wpilib.Wait(0.04)
            Robot.UpdateDashboard()

            if prevState != state:
                print("AUTO mode:%d state:%d" % (self.autoMode, state))
                deltaTime.Reset()
            prevState = state

            driveSpeed = 0.0
            driveTurn = 0.0

            if self.autoMode == 9:
                # fender 3-point
                if state == 0:
                    # Start delay
                    if deltaTime.Get() > self.startDelay:
                        state = 1
                elif state == 1:
                    Robot.shooter.SetupFenderElevation()
                    Robot.shooter.fenderMode = True

                    # Pre-rotate turret a bit to approximate where
                    # target will be
                    azstart = 0.0
                    if self.startPosition == self.LEFT:
                        azstart = 20.0
                    elif self.startPosition == self.RIGHT:
                        azstart = -20.0
                    Robot.shooter.azPid.SetSetpoint(azstart)
                    Robot.shooter.azPid.Enable()
                    state = 2
                elif state == 2:
                    # Drive forward
                    driveSpeed = None
                    Robot.drive.AutoDrive(0.75)
                    print("Drive encoder: %d" % Robot.rightDriveEncoder.Get())
                    if Robot.rightDriveEncoder.GetDistance() < -95:
                        state = 3
                elif state == 3:
                    # Stop driving
                    if deltaTime.Get() > 0.25:
                        state = 4
                elif state == 4:
                    Robot.shooter.Arm()
                    state = 5
                elif state == 5:
                    if deltaTime.Get() > 3.0:
                        state = 6
                elif state == 6:
                    Robot.shooter.Fire()
                    if deltaTime.Get() > 5.0:
                        state = 8
                elif state == 8:
                    Robot.shooter.StopFire()
                    Robot.shooter.StopArm()
            # Intake Two shoot 4 from the front corner
            if self.autoMode == 3:
                if state == 0:
                    #Start Delay
                    if deltaTime.Get() > self.startDelay:
                        state = 10
                elif state == 10:
                    Robot.arm.Lower()
                    state = 20
                elif state == 20:
                    if Robot.arm.IsDown():
                        state = 30
                elif state == 30:
                    pass
            # Shoot Two Front of pyramid
            if self.autoMode == 1:
                if state == 0:
                    # Start Delay
                    if deltaTime.Get() > self.startDelay:
                        state = 1
                elif state == 1:
                    Robot.arm.Lower()
                    state = 2
                elif state == 2:
                    if Robot.arm.IsDown():
                        state = 3
                elif state == 3:
                    Robot.elevation.SetHighFrontCenter()
                    state = 4
                elif state == 4:
                    Robot.shooter.SetHighFrontCenter()
                    Robot.shooter.Arm()
                    state = 5
                elif state == 5:
                    Robot.feeder.Run()
                    Robot.uptake.PositionForArming()
                    if Robot.elevation.OnTarget() and deltaTime.Get() > 4.0:
                        state = 6
                elif state == 6:
                    Robot.uptake.StartFiring()
                    if deltaTime.Get() > 8.0:
                        state = 7
                elif state == 7:
                    Robot.uptake.PositionForIntake()
                    state = 8
                elif state == 8:
                    Robot.uptake.Stop()
                    Robot.feeder.Stop()
                    Robot.shooter.StopArm()

            # Intake 2 Back Up shoot 4
            if self.autoMode == 2:
                if state == 0:
                    # Start Delay
                    if deltaTime.Get()> self.startDelay:
                        state = 10
                elif state == 10:
                    Robot.arm.Lower()
                    Robot.intake.Run()
                    Robot.conveyor.Run()
                    Robot.uptake.PositionForIntake()
                    state = 15
                elif state == 15:
                    pass
                elif state == 20:
                    driveSpeed = None
                    Robot.drive.AutoDrive(0.75)
                    if Robot.rightDriveEncoder.GetDistance() < 72:
                        state = 30
                elif state == 30:
                    driveSpeed = None
                    Robot.drive.AutoDrive(.75)
                    if Robot.rightDriveEncoder.GetDistance() < -72:
                        state = 40
                elif state == 40:
                    Robot.elevation.SetHighFrontCenter()
                    Robot.shooter.Arm()
                    Robot.shooter.SetHighFrontCenter()
                    state = 50
                elif state == 50:
                    Robot.shooter.Fire()
                    state = 60
                elif state == 60:
                    Robot.feeder.Run()
                    Robot.uptake.PositionForAiming()
                    state = 70
                elif state == 70:
                    Robot.uptake.StartFiring()
                    if deltaTime.Get() > 5.0:
                        state = 80
                elif state == 80:
                    Robot.uptake.PositionForIntake()
                    Robot.uptake.Stop()
                    Robot.feeder.Stop()
                    Robot.shooter.StopFiring()
                    Robot.shooter.StopArm()
                    state = 90

            if self.autoMode == 4:
                pass
            if self.autoMode == 5:
                pass
            if self.autoMode == 7:
                # test drive 4 feet
                if state == 0:
                    # Drive backward
                    driveSpeed = None
                    Robot.drive.AutoDrive(0.75)
                    print("Left encoder: %d" % Robot.leftDriveEncoder.Get())
                    print("Right encoder: %d" % Robot.rightDriveEncoder.Get())
                    if Robot.rightDriveEncoder.GetDistance() < -48:
                        state = 1

            Robot.intake.SetOutputs()
            Robot.conveyor.SetOutputs()
            Robot.uptake.SetOutputs()
            Robot.feeder.SetOutputs()
            Robot.elevation.SetOutputs()
            Robot.shooter.SetOutputs()

            # drive commands
            if driveSpeed is not None:
                Robot.drive.drive.ArcadeDrive(driveSpeed, driveTurn, False)
