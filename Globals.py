from wpilib import Preferences

__all__ = ["prefs"]

class Prefs:
    _types = dict(
            DriveTicksPerInch=float,
            ShooterFrontTestVolts=float,
            ShooterBackTestVolts=float,
             )

    def __init__(self):
        self._pref = Preferences.GetInstance()

    def __getattr__(self, name):
        cls = Prefs._types.get(name, eval)
        if issubclass(cls, bool):
            value = self._pref.GetBoolean(name)
        elif issubclass(cls, int):
            value = self._pref.GetLong(name)
        elif issubclass(cls, float):
            value = self._pref.GetDouble(name)
        else:
            value = cls(self._pref.GetString(name))
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
