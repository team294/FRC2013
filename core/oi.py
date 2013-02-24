import wpilib

class OI:
    @staticmethod
    def Init():
        # Joystick controls
        OI.leftStick = wpilib.Joystick(1)
        OI.rightStick = wpilib.Joystick(2)
        OI.coStick = wpilib.Joystick(3)
        OI.testStick = wpilib.Joystick(4)

        OI.ResetLastButtons()

    @staticmethod
    def ResetLastButtons():
        # last button status
        OI.lastLeftButtons = [False]*12
        OI.lastRightButtons = [False]*12
        OI.lastCoButtons = [False]*12
        OI.lastTestButtons = [False]*12
        OI.lastKinectButtons = [False]*12

    @staticmethod
    def UpdateLastButtons():
        for i in range(11):
            OI.lastLeftButtons[i+1] = OI.leftStick.GetRawButton(i+1)
            OI.lastRightButtons[i+1] = OI.rightStick.GetRawButton(i+1)
            OI.lastCoButtons[i+1] = OI.coStick.GetRawButton(i+1)
            OI.lastTestButtons[i+1] = OI.testStick.GetRawButton(i+1)

