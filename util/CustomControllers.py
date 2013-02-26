import wpilib
import threading

class CustomController:
    def __init__(self, source, output, period=0.05):
        self.mutex = threading.RLock()
        self.source = source
        self.output = output
        self.period = period
        self.enabled = False
        self.setpoint = 0
        self.error = 0
        self.result = 0
        self.controlLoop = wpilib.Notifier(self.Calculate)

    # PIDController-like interface
    def CalculateCallback(self, current, setpoint, result, error):
        pass

    def Enable(self):
        with self.mutex:
            self.enabled = True

    def Disable(self):
        self.output.PIDWrite(0)
        with self.mutex:
            self.enabled = False

    def IsEnabled(self):
        with self.mutex:
            return self.enabled

    def GetSetpoint(self):
        with self.mutex:
            return self.setpoint

    def SetSetpoint(self, setpoint):
        with self.mutex:
            self.setpoint = setpoint

    def GetError(self):
        with self.mutex:
            return self.setpoint - self.source.PIDGet()

class AccelDecelController(CustomController):
    def __init__(self, ramp_thres, source, output, period=0.05):
        super().__init__(source, output, period)
        self.ramp_thres = abs(ramp_thres)

    def Calculate(self):
        with self.mutex:
            enabled = self.enabled
            source = self.source

        if enabled:
            current = source.PIDGet()
            with self.mutex:
                self.error = self.setpoint - current
                if abs(self.error) > self.ramp_thres:
                    # Do full speed up until we hit the ramp threshold
                    if self.error > 0:
                        self.result = 1.0
                    else:
                        self.result = -1.0
                else:
                    # Linear scale to 0
                    self.result = (1.0 * self.error) / self.ramp_thres

                output = self.output
                result = self.result
                setpoint = self.setpoint
                error = self.error

            output.PIDWrite(result)
            self.CalculateCallback(current, setpoint, result, error)

    def SetRampThreshold(self, ramp_thres):
        with self.mutex:
            self.ramp_thres = ramp_thres

