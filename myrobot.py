import wpilib
from core import *
from subsystems import *
from autonomous import *
from operator_control import *
import logging

class MyRobot(wpilib.SimpleRobot):
    def __init__(self):
        super().__init__()

        # Create Subsystems
        logging.info("Creating subsystems")
        Robot.AddSubsystem("arm", RobotArm)
        Robot.AddSubsystem("drive", RobotDrive)
        Robot.AddSubsystem("feeder", RobotFeeder)
        Robot.AddSubsystem("intake", RobotIntake)
        Robot.AddSubsystem("shooter", RobotShooter)
        Robot.AddSubsystem("conveyor", RobotConveyor)
        Robot.AddSubsystem("elevation", RobotElevation)
        Robot.AddSubsystem("uptake", RobotUptake)

        #StartImageServer()
        logging.info("Creating auto/operator")
        self.auto = Autonomous()
        self.operator = OperatorControl()

    def RobotInit(self):
        wpilib.Wait(0.1)
        Robot.InitSubsystems()

    def Disabled(self):
        logging.info("Starting Disabled()")
        self.auto.DisplayMode()

        while self.IsDisabled():
            self.auto.ModeSelection()
            OI.UpdateLastButtons()
            wpilib.Wait(0.01)

    def Autonomous(self):
        logging.info("Starting Autonomous()")
        Robot.InitSubsystems()
        try:
            self.auto.Run()
        except:
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)
            while self.IsAutonomous() and self.IsEnabled():
                wpilib.Wait(0.04)

    def OperatorControl(self):
        logging.info("Starting OperatorControl()")
        Robot.InitSubsystems()
        try:
            self.operator.Run()
        except:
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)
            while self.IsOperatorControl() and self.IsEnabled():
                wpilib.Wait(0.04)
