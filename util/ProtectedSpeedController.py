import wpilib
import threading
import time

class ProtectedSpeedController(wpilib.SpeedController):
    def __init__(self, output, limit=30.0):
        super().__init__()
        self.output = output
        self.limit = limit
        self.failed = False
        self.mutex = threading.RLock()
        self.thread = threading.Thread(target=self.Check)
        self.thread.start()

    def Check(self):
        count = 0
        while True:
            if self.output.GetOutputCurrent() > self.limit:
                count += 1
            else:
                count = 0
            if count > 5:
                with self.mutex:
                    self.failed = True
                self.output.Set(0.0)
                print("Hit failsafe!!!")
            time.sleep(0.1)

    def Get(self):
        return self.output.Get()

    def Set(self, value, syncGroup=0):
        with self.mutex:
            if self.failed:
                return
        self.output.Set(value, syncGroup)

    def Disable(self):
        self.output.Disable()

    def PIDWrite(self, output):
        with self.mutex:
            if self.failed:
                return
        self.output.PIDWrite(output)

    def GetOutputCurrent(self):
        return self.output.GetOutputCurrent()
