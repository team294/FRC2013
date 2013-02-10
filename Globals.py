from wpilib import Preferences

__all__ = ["prefs"]

class Prefs:
    _types = dict(
            DriveTicksPerInch=float,
             )

    def __init__(self):
        self._value_cache = {}

    def __getattr__(self, name):
        pref = Preferences.GetInstance()
        if pref.changed:
            self._value_cache.clear()
        value = self._value_cache.get(name)
        if value is not None:
            return value
        value = pref.Get(name)
        if value is None:
            raise AttributeError
        cls = Prefs._types.get(name, eval)
        value = cls(value)
        self._value_cache[name] = value
        return value

    def __setattr__(self, name, value):
        if name[0] == '_':
            object.__setattr__(self, name, value)
        else:
            pref = Preferences.GetInstance()
            if isinstance(value, bool):
                pref.PutBoolean(name, value)
            else:
                pref.Put(name, str(value))

prefs = Prefs()
