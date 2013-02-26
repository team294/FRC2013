from wpilib import Preferences

__all__ = ["prefs"]

class Prefs:
    _types = dict(
            DriveTicksPerInch=float,
            ShooterFrontTestVolts=float,
            ShooterBackTestVolts=float,
            ShooterFrontHighFrontCenterVolts=float,
            ShooterBackHighFrontCenterVolts=float,
            ShooterFrontHighFrontCornerVolts=float,
            ShooterBackHighFrontCornerVolts=float,
            UptakeP=float,
            UptakeI=float,
            UptakeD=float,
            UptakeBottomLimit=int,
            UptakeTopLimit=int,
            UptakeIntakeP=float,
            UptakeIntakeI=float,
            UptakeIntakeD=float,
            UptakeIntakeOutputRange=float,
            UptakeIntakeSetpoint=int,
            UptakeArmP=float,
            UptakeArmI=float,
            UptakeArmD=float,
            UptakeArmOutputRange=float,
            UptakeArmSetpoint=int,
            UptakeFireP=float,
            UptakeFireI=float,
            UptakeFireD=float,
            UptakeFireOutputRange=float,
            UptakeFireSetpoint=int,
            ElevRampThres=float,
            ElevBottomLimit=int,
            ElevTopLimit=int,
            ElevUnderPyramidSetpoint=int,
            ElevHighFrontCenterSetpoint=int,
            ElevHighFrontCornerSetpoint=int,
            ElevHighBackCenterSetpoint=int,
            ElevPyramidSetpoint=int,
            ElevStartSetpoint=int,
             )

    def __init__(self):
        self._pref = Preferences.GetInstance()

    def __getattr__(self, name):
        cls = Prefs._types.get(name, str)
        if issubclass(cls, bool):
            value = self._pref.GetBoolean(name)
        elif issubclass(cls, int):
            value = self._pref.GetLong(name)
        elif issubclass(cls, float):
            value = self._pref.GetDouble(name)
        else:
            value = eval(self._pref.GetString(name))
        return value

    def __setattr__(self, name, value):
        if name[0] == '_':
            object.__setattr__(self, name, value)
        else:
            if isinstance(value, bool):
                self._pref.PutBoolean(name, value)
            elif isinstance(value, int):
                self._pref.PutLong(name, value)
            elif isinstance(value, float):
                self._pref.PutDouble(name, value)
            else:
                self._pref.PutString(name, str(value))

prefs = Prefs()
