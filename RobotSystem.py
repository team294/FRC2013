import wpilib
from util.DualSpeedController import *
from util.LimitedSpeedController import *
from util.ProtectedSpeedController import *

# Joystick controls
leftStick = wpilib.Joystick(1)
rightStick = wpilib.Joystick(2)
coStick = wpilib.Joystick(3)
testStick = wpilib.Joystick(4)
class RobotSystem:
    @staticmethod
    def GetInstance():
        try:
            return RobotSystem._instance
        except AttributeError:
            RobotSystem._instance = RobotSystem._inner()
            return RobotSystem._instance

    class _inner:
        def __init__(self):
            ### Jaguars
            #Left Drive
            self.leftTopMotor = wpilib.CANJaguar(7)
            self.leftBottomMotor = wpilib.CANJaguar(6)
            self.leftMotor = DualSpeedController(self.leftTopMotor, self.leftBottomMotor, 1)
            #Right Drive
            self.rightTopMotor = wpilib.CANJaguar(3)
            self.rightBottomMotor = wpilib.CANJaguar(4)
            self.rightMotor = DualSpeedController(self.rightTopMotor, self.rightBottomMotor, 1)

            #shooter
            self.shooterFrontMotor = wpilib.CANJaguar(1, wpilib.CANJaguar.kVoltage)
            self.shooterBackMotor = wpilib.CANJaguar(2, wpilib.CANJaguar.kVoltage)
            self.elevationMotorUnlimited = wpilib.CANJaguar(5)

            ### Victors
            self.intakeMotor = wpilib.Victor(1)
            self.conveyorMotor = wpilib.Victor(2)
            self.uptakeMotorUnlimited = wpilib.Victor(3)
            self.feederMotor = wpilib.Victor(4)

            ### Inputs
            self.rightDriveEncoder = wpilib.Encoder(2,3)
            self.leftDriveEncoder = wpilib.Encoder(4,5,False)
            self.discIn = wpilib.DigitalInput(6)
            self.discOut = wpilib.DigitalInput(8)
            self.shooterCounterBack = wpilib.Counter(9)
            self.shooterCounterFront = wpilib.Counter(10)
            self.uptakePot = wpilib.AnalogChannel(2)
            self.elevationPot = wpilib.AnalogChannel(3)

            self.gyro = wpilib.Gyro(1)

            ### Solenoids
            self.shifterUp = wpilib.Solenoid(1)
            self.shifterDown = wpilib.Solenoid(2)
            self.armUp = wpilib.Solenoid(3)
            self.armDown = wpilib.Solenoid(4)
            self.flipper1 = wpilib.Solenoid(5)
            self.flipper2 = wpilib.Solenoid(6)
            self.climb1 = wpilib.Solenoid(7)
            self.climb2 = wpilib.Solenoid(8)

            ### Compressor
            self.compressor = wpilib.Compressor(1,1)

            ### Limited motors
            ##self.elevationMotor = PotLimitedSpeedController(self.elevationMotorUnlimited, self.elevationPot,
                    ##"ElevationTopLimit", "ElevationBottomLimit")
            self.uptakeMotor = PotLimitedSpeedController(
                    self.uptakeMotorUnlimited,
                    self.uptakePot,
                    "UptakeTopLimit",
                    "UptakeBottomLimit",
                    inverted=True)

            ### Dashboard
            self.db = wpilib.DriverStation.GetInstance().GetLowPriorityDashboardPacker()

            # last button status
            self.lastLeftButtons = [False]*12
            self.lastRightButtons = [False]*12
            self.lastCoButtons = [False]*12
            self.lastTestButtons = [False]*12
            self.lastKinectButtons = [False]*12

        def CreateSubsystems(self):
            # Subsystems
            print("Creating subsystems")
            from Arm import RobotArm
            from Drive import RobotDrive
            from Feeder import RobotFeeder
            from Intake import RobotIntake
            from Shooter import RobotShooter
            from Conveyor import RobotConveyor
            from Elevation import RobotElevation
            from Uptake import RobotUptake

            self.arm = RobotArm()
            self.drive = RobotDrive()
            self.feeder = RobotFeeder()
            self.intake = RobotIntake()
            self.shooter = RobotShooter()
            self.conveyor = RobotConveyor()
            self.elevation = RobotElevation()
            self.uptake = RobotUptake()

        def Init(self):
            # Init subsystems
            print("Initializing")
            self.leftTopMotor.SetVoltageRampRate(24.0/0.2)
            self.leftBottomMotor.SetVoltageRampRate(24.0/0.2)
            self.rightTopMotor.SetVoltageRampRate(24.0/0.2)
            self.rightBottomMotor.SetVoltageRampRate(24.0/0.2)
            self.arm.Init()
            self.drive.Init()
            self.conveyor.Init()
            self.intake.Init()
            self.shooter.Init()
            self.feeder.Init()
            self.uptake.Init()
            self.elevation.Init()

            self.lastLeftButtons = [False]*12
            self.lastRightButtons = [False]*12
            self.lastCoButtons = [False]*12
            self.lastTestButtons = [False]*12

        def UpdateLastButtons(self):
            for i in range(11):
                self.lastLeftButtons[i+1] = leftStick.GetRawButton(i+1)
                self.lastRightButtons[i+1] = rightStick.GetRawButton(i+1)
                self.lastCoButtons[i+1] = coStick.GetRawButton(i+1)
                self.lastTestButtons[i+1] = testStick.GetRawButton(i+1)

        def Disabled(self):
            self.UpdateLastButtons()

        def OperatorControl(self):
            # Run subsystems
            self.arm.OperatorControl()
            self.drive.OperatorControl()
            self.conveyor.OperatorControl()
            self.intake.OperatorControl()
            self.shooter.OperatorControl()
            self.uptake.OperatorControl()
            self.feeder.OperatorControl()
            self.elevation.OperatorControl()

            self.UpdateLastButtons()

        def UpdateDashboard(self):
            # Collect and send dashboard information
            #self.db.AddCluster()
            #self.shooter.UpdateDashboard(self.db)
            #self.db.FinalizeCluster()
            #self.db.Finalize()
            pass

robot = RobotSystem.GetInstance()
