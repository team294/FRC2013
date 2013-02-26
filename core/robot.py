import wpilib
import logging
from util.DualSpeedController import *
from util.LimitedSpeedController import *
from util.ProtectedSpeedController import *

class Robot:
    @staticmethod
    def Init():
        ### Jaguars
        logging.info("Creating Jaguars")
        #Left Drive
        Robot.leftTopMotor = wpilib.CANJaguar(7)
        Robot.leftBottomMotor = wpilib.CANJaguar(6)
        Robot.leftMotor = DualSpeedController(Robot.leftTopMotor, Robot.leftBottomMotor, 1)
        #Right Drive
        Robot.rightTopMotor = wpilib.CANJaguar(3)
        Robot.rightBottomMotor = wpilib.CANJaguar(4)
        Robot.rightMotor = DualSpeedController(Robot.rightTopMotor, Robot.rightBottomMotor, 1)

        #shooter
        Robot.shooterFrontMotor = wpilib.CANJaguar(1, wpilib.CANJaguar.kVoltage)
        Robot.shooterBackMotor = wpilib.CANJaguar(2, wpilib.CANJaguar.kVoltage)
        Robot.elevationMotorUnlimited = wpilib.CANJaguar(5)

        ### Victors
        logging.info("Creating Victors")
        Robot.intakeMotor = wpilib.Victor(1)
        Robot.conveyorMotor = wpilib.Victor(2)
        Robot.uptakeMotorUnlimited = wpilib.Victor(3)
        Robot.feederMotor = wpilib.Victor(4)

        ### Inputs
        logging.info("Creating inputs")
        Robot.rightDriveEncoder = wpilib.Encoder(2,3)
        Robot.leftDriveEncoder = wpilib.Encoder(4,5,False)
        Robot.discIn = wpilib.DigitalInput(6)
        Robot.discOut = wpilib.DigitalInput(8)
        Robot.backShooterCounter = wpilib.Counter(9)
        Robot.frontShooterCounter = wpilib.Counter(10)
        Robot.uptakePot = wpilib.AnalogChannel(2)
        Robot.elevationPot = wpilib.AnalogChannel(3)

        logging.info("Starting gyro")
        Robot.gyro = wpilib.Gyro(1)

        ### Solenoids
        logging.info("Creating solenoids")
        Robot.shifterPiston = wpilib.DoubleSolenoid(1, 2)
        Robot.armPiston = wpilib.DoubleSolenoid(3, 4)
        Robot.flipperPiston = wpilib.DoubleSolenoid(5, 6)
        Robot.climbPiston = wpilib.DoubleSolenoid(7, 8)

        ### Compressor
        logging.info("Starting compressor")
        Robot.compressor = wpilib.Compressor(1,1)
        Robot.compressor.Start()

        ### Limited motors
        logging.info("Creating limited motors")
        Robot.elevationMotor = PotLimitedSpeedController(
                Robot.elevationMotorUnlimited,
                Robot.elevationPot,
                "ElevBottomLimit",
                "ElevTopLimit",
                inverted=True)
        Robot.uptakeMotor = PotLimitedSpeedController(
                Robot.uptakeMotorUnlimited,
                Robot.uptakePot,
                "UptakeTopLimit",
                "UptakeBottomLimit",
                inverted=True)

        ### Dashboard
        logging.info("Configuring dashboard")
        Robot.db = wpilib.DriverStation.GetInstance().GetLowPriorityDashboardPacker()

        Robot.subsystems = []

    @staticmethod
    def AddSubsystem(name, cls):
        logging.info("Creating subsystem %s (%s)", name, cls.__name__)
        val = cls()
        setattr(Robot, name, val)
        Robot.subsystems.append(val)

    @staticmethod
    def InitSubsystems():
        # Init subsystems
        logging.info("Initializing subsystems")
        for ss in Robot.subsystems:
            ss.Init()

    @staticmethod
    def UpdateDashboard():
        # Collect and send dashboard information
        #Robot.db.AddCluster()
        #Robot.shooter.UpdateDashboard(Robot.db)
        #Robot.db.FinalizeCluster()
        #Robot.db.Finalize()
        pass
