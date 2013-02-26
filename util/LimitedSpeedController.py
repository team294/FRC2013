import wpilib
import logging

class PotLimitedSpeedController(wpilib.SpeedController):
    def __init__(self, output, pot, lowLimitPref, highLimitPref, inverted=False, failsafe=True):
        super().__init__()
        self.output = output
        self.pot = pot
        self.lowLimitPref = lowLimitPref
        self.highLimitPref = highLimitPref
        self.inverted = inverted
        self.failsafe = failsafe
        self.prefs = wpilib.Preferences.GetInstance()

    def Set(self, speed, syncGroup=0):
        potValue = self.pot.GetValue()
        lowLimit = self.prefs.GetDouble(self.lowLimitPref)
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
