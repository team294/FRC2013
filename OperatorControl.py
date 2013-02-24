import wpilib
from RobotSystem import *

class OperatorControl:
    def Run(self):
        robot.ResetLastButtons()
        wpilib.GetWatchdog().SetExpiration(0.2)
        wpilib.GetWatchdog().SetEnabled(True)

        # Startup conditions for teleop
        robot.intake.Stop()
        robot.conveyor.Stop()
        #robot.uptake.PositionForIntake()
        robot.feeder.Stop()
        robot.shooter.Stop()

        frame = 0
        prevArmed = False
        prevFiring = False
        while wpilib.IsOperatorControl() and wpilib.IsEnabled():
            wpilib.GetWatchdog().Feed()
            wpilib.Wait(0.04)
            robot.UpdateDashboard()
            robot.UpdateLastButtons()

            if frame % 20 == 1:
                print("gyroAngle:   %f" % robot.gyro.GetAngle())
                print("dumbyPot:   %f" % robot.uptakePot.GetAverageValue())
                print("elPot:   %f" % robot.elevationPot.GetAverageValue())
                print("lEnc:    %d" % robot.leftDriveEncoder.Get())
                print("rEnc:    %d" % robot.rightDriveEncoder.Get())
            frame+= 1

            ###################
            # DRIVER CONTROLS #
            ###################

            # Drive shifters
            if leftStick.GetTrigger():
                robot.drive.ShiftDown()
            if rightStick.GetTrigger():
                robot.drive.ShiftUp()

            # Drive control
            lPower = leftStick.GetY()
            rPower = rightStick.GetY()
            robot.drive.TankDrive(lPower, rPower)

            #####################
            # CODRIVER CONTROLS #
            #####################

            # Arm
            if coStick.GetRawButton(6):
                robot.arm.Raise()
            if coStick.GetRawButton(7):
                robot.arm.Lower()

            # Intake and Conveyor run together
            if coStick.GetRawButton(10):
                robot.intake.Run()
                robot.conveyor.Run()
            if coStick.GetRawButton(11):
                robot.intake.Stop()
                robot.conveyor.Stop()

            # Override intake to stop if the uptake isn't in the right
            # position
            if not robot.uptake.InIntakePosition():
                robot.intake.Stop()
                robot.conveyor.Stop()

            # Uptake / Feeder / Shooter
            armed = coStick.GetRawButton(2)
            firing = coStick.GetRawButton(1)
            if not armed:
                firing = False

            # arming moves the uptake, and starts the shooter
            if armed and not prevArmed:
                robot.uptake.PositionForArming()
                robot.shooter.SetTestSpeed() # TODO

            # firing starts the feeder, and moves the uptake after some delay
            if firing and not prevFiring:
                robot.feeder.Run()
                robot.uptake.StartFiring()

            # if we stopped firing, stop the feeder and uptake movement
            if prevFiring and not firing:
                robot.feeder.Stop()
                robot.uptake.Stop()

            # if we unarmed, the uptake should go to intake position and
            # the shooter and feeder should stop running
            if prevArmed and not armed:
                robot.uptake.PositionForIntake()
                robot.feeder.Stop()
                robot.shooter.Stop()

            #################
            # TEST CONTROLS #
            #################

            # Arm
            if testStick.GetRawButton(6):
                robot.arm.Raise()
            if testStick.GetRawButton(7):
                robot.arm.Lower()

            # Intake
            # clicking the button stops/starts
            if testStick.GetRawButton(11) and not robot.lastTestButtons[11]:
                robot.intake.running = not robot.intake.running

            # Conveyor
            # clicking the button stops/starts
            if testStick.GetRawButton(2) and not robot.lastTestButtons[2]:
                self.conveyor.running = not self.conveyor.running

            # Uptake
            mval = 0
            if testStick.GetRawButton(3):
                mval = testStick.GetY()/2.0
                robot.uptake.pid.Disable()

            if not robot.uptake.pid.IsEnabled():
                robot.uptakeMotor.Set(mval)

            # Elevation
            if testStick.GetRawButton(8):
                robot.elevationMotorUnlimited.Set(testStick.GetY())
            else:
                robot.elevationMotorUnlimited.Set(0)

            # Feeder
            # clicking the button stops/starts
            if testStick.GetRawButton(5) and not robot.lastTestButtons[5]:
                robot.feeder.running = not robot.feeder.running

            # Shooter
            if testStick.GetRawButton(10):
                robot.shooter.SetTestSpeed()
            else:
                robot.shooter.Stop()

            ########################
            # DRIVE NON-PID MOTORS #
            ########################

            robot.intake.SetOutputs()
            #robot.elevation.SetOutputs()
            robot.conveyor.SetOutputs()
            robot.feeder.SetOutputs()
            robot.shooter.SetOutputs()

            # State variables
            prevArmed = armed
            prevFiring = firing
