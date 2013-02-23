import wpilib
from RobotSystem import *
from Autonomous import *
#from ImageProcessing import StartImageServer
from wpilib import SmartDashboard

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING)

class MyRobot(wpilib.SimpleRobot):
    def __init__(self):
        super().__init__()
        #SmartDashboard.GetInstance()
        robot.CreateSubsystems()
        #StartImageServer()
        robot.compressor.Start()
        self.auto = Autonomous()

    def RobotInit(self):
        wpilib.Wait(0.1)
        robot.Init()

    def Disabled(self):
        self.auto.DisplayMode()

        while self.IsDisabled():
            self.auto.ModeSelection()
            robot.Disabled()
            wpilib.Wait(0.01)

    def Autonomous(self):
        try:
            self.auto.Run()
        except:
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)
            while self.IsAutonomous() and self.IsEnabled():
                wpilib.Wait(0.04)

    def OperatorControl(self):
        wpilib.GetWatchdog().SetExpiration(0.2)
        wpilib.GetWatchdog().SetEnabled(True)
        robot.Init()

        frame = 0
        while self.IsOperatorControl() and self.IsEnabled():
            wpilib.GetWatchdog().Feed()
            robot.OperatorControl()
            robot.UpdateDashboard()
            wpilib.Wait(0.04)

            if frame % 20 == 1:
                print("gyroAngle:   %f" % robot.gyro.GetAngle())
                print("dumbyPot:   %f" % robot.uptakePot.GetAverageValue())
                print("elPot:   %f" % robot.elevationPot.GetAverageValue())
                print("lEnc:    %d" % robot.leftDriveEncoder.Get())
                print("rEnc:    %d" % robot.rightDriveEncoder.Get())
            frame+= 1

def run():
    logging.debug("starting run()")
    myRobot = MyRobot()
    myRobot.StartCompetition()
