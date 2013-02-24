import logging

logging.info("Importing wpilib")
import wpilib
logging.info("Importing core")
from core import *
from myrobot import *

def run():
    logging.info("Starting run()")
    logging.info("Initializing Robot")
    Robot.Init()
    logging.info("Initializing OI")
    OI.Init()
    robot = MyRobot()
    logging.info("Starting competition")
    robot.StartCompetition()
