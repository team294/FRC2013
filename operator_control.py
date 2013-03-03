import wpilib
from core import *

class OperatorControl:
    def Run(self):
        OI.ResetLastButtons()
        wpilib.GetWatchdog().SetExpiration(0.2)
        wpilib.GetWatchdog().SetEnabled(True)

        # Startup conditions for teleop
        Robot.intake.Stop()
        Robot.conveyor.Stop()
        Robot.uptake.StopFiring()
        Robot.uptake.PositionForIntake()
        Robot.feeder.Stop()
        Robot.shooter.StopArm()

        frame = 0
        prevArmed = False
        prevFiring = False
        while wpilib.IsOperatorControl() and wpilib.IsEnabled():
            wpilib.GetWatchdog().Feed()
            wpilib.Wait(0.04)
            Robot.UpdateDashboard()

            if frame % 20 == 1:
                logging.info("gyroAngle:   %f", Robot.gyro.GetAngle())
                logging.info("uptakePot:   %f", Robot.uptakePot.GetAverageValue())
                logging.info("elvPot:   %f", Robot.elevationPot.GetAverageValue())
                logging.info("lEnc:    %d", Robot.leftDriveEncoder.Get())
                logging.info("rEnc:    %d", Robot.rightDriveEncoder.Get())
            frame+= 1

            ###################
            # DRIVER CONTROLS #
            ###################

            # Drive shifters
            if OI.leftStick.GetTrigger():
                Robot.drive.ShiftDown()
            if OI.rightStick.GetTrigger():
                Robot.drive.ShiftUp()

            # Drive control
            lPower = OI.leftStick.GetY()
            rPower = OI.rightStick.GetY()
            Robot.drive.TankDrive(lPower, rPower)

            #####################
            # CODRIVER CONTROLS #
            #####################

            # Arm
            if OI.coStick.GetRawButton(6):
                Robot.arm.Raise()
            if OI.coStick.GetRawButton(7):
                Robot.arm.Lower()

            # Intake and Conveyor run together
            if OI.coStick.GetRawButton(10):
                Robot.intake.Run()
                Robot.conveyor.Run()
            if OI.coStick.GetRawButton(11):
                Robot.intake.Stop()
                Robot.conveyor.Stop()

            # Override intake to stop if the uptake isn't in the right
            # position or the arm is up
            #if not Robot.uptake.InIntakePosition() or not Robot.arm.IsDown():
            #    Robot.intake.Stop()
            #    Robot.conveyor.Stop()

            # Elevation
            #if OI.coStick.GetRawButton(4):
            #    Robot.elevation.GoUnderPyramid()
            #elif OI.coStick.GetRawButton(3):
            #    Robot.elevation.SetHighFrontCenter()
            #elif OI.coStick.GetRawButton(5):
            #    Robot.elevation.SetStartPosition()

            # Uptake / Feeder / Shooter
            armed = OI.coStick.GetRawButton(2)
            firing = OI.coStick.GetRawButton(1)
            # can't fire until on target
            if not Robot.shooter.OnTarget() or not Robot.elevation.OnTarget():
                firing = False
            if not armed:
                firing = False

            # arming moves the uptake, and starts the shooter
            # also stops intaking
            if armed and not prevArmed:
                Robot.intake.Stop()
                Robot.conveyor.Stop()
                Robot.uptake.PositionForArming()
                Robot.elevation.SetHighFrontCenter()
                Robot.shooter.SetHighFrontCenter() # TODO
                Robot.shooter.Arm()

            # firing starts the feeder, and moves the uptake after some delay
            if firing and not prevFiring:
                Robot.feeder.Run()
                Robot.uptake.StartFiring()

            # if we stopped firing, stop the feeder and uptake movement
            if prevFiring and not firing:
                Robot.feeder.Stop()
                Robot.uptake.PositionForArming()
                Robot.uptake.StopFiring()

            # if we unarmed, the uptake should go to intake position and
            # the shooter and feeder should stop running
            # We also start running the intake again
            if prevArmed and not armed:
                Robot.uptake.PositionForIntake()
                Robot.feeder.Stop()
                Robot.shooter.StopArm()
                Robot.elevation.GoHome()
                Robot.intake.Run()

            # Manual Uptake
            if OI.coStick.GetRawButton(3):
                Robot.uptake.SetManual(OI.coStick.GetY()/2.0)
            if not OI.coStick.GetRawButton(3) and OI.lastCoButtons[3]:
                Robot.uptake.SetManual(None)

            # Manual Elevation (tweak)
            if OI.coStick.GetRawButton(4) and not OI.lastCoButtons[4]:
                Robot.elevation.TweakDown()
            if OI.coStick.GetRawButton(5) and not OI.lastCoButtons[5]:
                Robot.elevation.TweakUp()

            #################
            # TEST CONTROLS #
            #################

            # Arm
            if OI.testStick.GetRawButton(6):
                Robot.arm.Raise()
            if OI.testStick.GetRawButton(7):
                Robot.arm.Lower()

            # Intake
            # clicking the button stops/starts
            if OI.testStick.GetRawButton(11) and not OI.lastTestButtons[11]:
                Robot.intake.running = not Robot.intake.running

            # Conveyor
            # clicking the button stops/starts
            if OI.testStick.GetRawButton(2) and not OI.lastTestButtons[2]:
                Robot.conveyor.running = not Robot.conveyor.running

            # Uptake
            if OI.testStick.GetRawButton(3) and not OI.lastTestButtons[3]:
                Robot.uptake.SetManual(OI.testStick.GetY()/2.0)
            if not OI.testStick.GetRawButton(3) and OI.lastTestButtons[3]:
                Robot.uptake.SetManual(None)

            # Elevation
            if OI.testStick.GetRawButton(8):
                Robot.elevation.SetManual(OI.testStick.GetY())
            if not OI.testStick.GetRawButton(8) and OI.lastTestButtons[8]:
                Robot.elevation.SetManual(None)

            # Feeder
            # clicking the button stops/starts
            if OI.testStick.GetRawButton(5) and not OI.lastTestButtons[5]:
                Robot.feeder.running = not Robot.feeder.running

            # Shooter
            if OI.testStick.GetRawButton(10):
                Robot.shooter.SetTestSpeed()
                Robot.shooter.Arm()
            elif not OI.testStick.GetRawButton(10) and OI.lastTestButtons[10]:
                Robot.shooter.StopArm()

            ########################
            # DRIVE NON-PID MOTORS #
            ########################

            Robot.intake.SetOutputs()
            Robot.conveyor.SetOutputs()
            Robot.uptake.SetOutputs()
            Robot.feeder.SetOutputs()
            Robot.elevation.SetOutputs()
            Robot.shooter.SetOutputs()

            # State variables
            prevArmed = armed
            prevFiring = firing

            OI.UpdateLastButtons()

