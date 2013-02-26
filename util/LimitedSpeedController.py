import wpilib
import threading
import logging

class PotLimitedSpeedController(wpilib.SpeedController):
    def __init__(self, output, pot, lowLimitPref, highLimitPref, inverted=False, failsafe=True):
        super().__init__()
        self.mutex = threading.RLock()
        self.output = output
        self.pot = pot
        self.lowLimitPref = lowLimitPref
        self.highLimitPref = highLimitPref
        self.forcedLowLimit = None
        self.forcedHighLimit = None
        self.inverted = inverted
        self.failsafe = failsafe
        self.prefs = wpilib.Preferences.GetInstance()

    def ForceLowLimit(self, limit):
        with self.mutex:
            self.forcedLowLimit = limit

    def ForceHighLimit(self, limit):
        with self.mutex:
            self.forcedHighLimit = limit

    def Set(self, speed, syncGroup=0):
        potValue = self.pot.GetValue()
        with self.mutex:
            if self.forcedLowLimit is not None:
                lowLimit = self.forcedLowLimit
            else:
                lowLimit = self.prefs.GetDouble(self.lowLimitPref)
            if self.forcedHighLimit is not None:
                highLimit = self.forcedHighLimit
            else:
                highLimit = self.prefs.GetDouble(self.highLimitPref)
        #if lowLimit > highLimit:
        #    lowLimit, highLimit = highLimit, lowLimit
        #logging.debug("speed: %f value: %d lowLimit: %d highLimit: %d inv: %d", speed, potValue, lowLimit, highLimit, self.inverted)
        # if pot disconnected, don't let it drive at all
        if self.failsafe and potValue < 0:
            self.output.Set(0, syncGroup)
            return
        if not self.inverted:
            if speed < 0 and potValue < lowLimit:
                self.output.Set(0, syncGroup)
            elif speed > 0 and potValue > highLimit:
                self.output.Set(0, syncGroup)
            else:
                self.output.Set(speed, syncGroup)
        else:
            if speed > 0 and potValue < lowLimit:
                self.output.Set(0, syncGroup)
            elif speed < 0 and potValue > highLimit:
                self.output.Set(0, syncGroup)
            else:
                self.output.Set(speed, syncGroup)

    def Get(self):
        return self.output.Get()

    def Disable(self):
        self.output.Disable()
