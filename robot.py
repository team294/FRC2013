import wpilib
from RobotSystem import *
from Autonomous import *
from OperatorControl import *
#from ImageProcessing import StartImageServer
from wpilib import SmartDashboard

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING)

class MyRobot(wpilib.SimpleRobot):
    def __init__(self):
        super().__init__()
        SmartDashboard.init()
        robot.CreateSubsystems()
        #StartImageServer()
        robot.compressor.Start()
        self.auto = Autonomous()
        self.operator = OperatorControl()

    def RobotInit(self):
        wpilib.Wait(0.1)
        robot.Init()

    def Disabled(self):
        self.auto.DisplayMode()

        while self.IsDisabled():
            self.auto.ModeSelection()
            robot.UpdateLastButtons()
            wpilib.Wait(0.01)

    def Autonomous(self):
        robot.Init()
        try:
            self.auto.Run()
        except:
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)
            while self.IsAutonomous() and self.IsEnabled():
                wpilib.Wait(0.04)

    def OperatorControl(self):
        robot.Init()
        try:
            self.operator.Run()
        except:
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)
            while self.IsOperatorControl() and self.IsEnabled():
                wpilib.Wait(0.04)

def run():
    logging.debug("starting run()")
    myRobot = MyRobot()
    myRobot.StartCompetition()
