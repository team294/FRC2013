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
        #Robot.uptake.PositionForIntake()
        Robot.feeder.Stop()
        Robot.shooter.Stop()

        frame = 0
        prevArmed = False
        prevFiring = False
        while wpilib.IsOperatorControl() and wpilib.IsEnabled():
            wpilib.GetWatchdog().Feed()
            wpilib.Wait(0.04)
            Robot.UpdateDashboard()

            if frame % 20 == 1:
                print("gyroAngle:   %f" % Robot.gyro.GetAngle())
                print("uptakePot:   %f" % Robot.uptakePot.GetAverageValue())
                print("elvPot:   %f" % Robot.elevationPot.GetAverageValue())
                print("lEnc:    %d" % Robot.leftDriveEncoder.Get())
                print("rEnc:    %d" % Robot.rightDriveEncoder.Get())
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
            if not Robot.uptake.InIntakePosition() or not Robot.arm.IsDown():
                Robot.intake.Stop()
                Robot.conveyor.Stop()

            # Uptake / Feeder / Shooter
            armed = OI.coStick.GetRawButton(2)
            firing = OI.coStick.GetRawButton(1)
            if not armed:
                firing = False

            # arming moves the uptake, and starts the shooter
            if armed and not prevArmed:
                Robot.uptake.PositionForArming()
                Robot.shooter.SetTestSpeed() # TODO

            # firing starts the feeder, and moves the uptake after some delay
            if firing and not prevFiring:
                Robot.feeder.Run()
                Robot.uptake.StartFiring()

            # if we stopped firing, stop the feeder and uptake movement
            if prevFiring and not firing:
                Robot.feeder.Stop()
                Robot.uptake.Stop()

            # if we unarmed, the uptake should go to intake position and
            # the shooter and feeder should stop running
            if prevArmed and not armed:
                Robot.uptake.PositionForIntake()
                Robot.feeder.Stop()
                Robot.shooter.Stop()

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
            mval = 0
            if OI.testStick.GetRawButton(3):
                mval = OI.testStick.GetY()/2.0
                Robot.uptake.pid.Disable()

            if not Robot.uptake.pid.IsEnabled():
                Robot.uptakeMotor.Set(mval)

            # Elevation
            if OI.testStick.GetRawButton(8):
                Robot.elevationMotorUnlimited.Set(OI.testStick.GetY())
            else:
                Robot.elevationMotorUnlimited.Set(0)

            # Feeder
            # clicking the button stops/starts
            if OI.testStick.GetRawButton(5) and not OI.lastTestButtons[5]:
                Robot.feeder.running = not Robot.feeder.running

            # Shooter
            if OI.testStick.GetRawButton(10):
                Robot.shooter.SetTestSpeed()
            else:
                Robot.shooter.Stop()

            ########################
            # DRIVE NON-PID MOTORS #
            ########################

            Robot.intake.SetOutputs()
            #Robot.elevation.SetOutputs()
            Robot.conveyor.SetOutputs()
            Robot.feeder.SetOutputs()
            Robot.shooter.SetOutputs()

            # State variables
            prevArmed = armed
            prevFiring = firing

            OI.UpdateLastButtons()

