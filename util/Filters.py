import wpilib
import threading

class SlidingWindowAverageFilter:
    def __init__(self, srcfcn, nsamples, period=0.01):
        self.mutex = threading.RLock()
        self.srcfcn = srcfcn
        self.nsamples = nsamples
        self.samples = [0]*nsamples
        self.controlLoop = wpilib.Notifier(self.Update)
        self.controlLoop.StartPeriodic(period)

    def Update(self):
        with self.mutex:
            del self.samples[0]
            self.samples.append(self.srcfcn())

    def GetAverage(self):
        with self.mutex:
            return sum(self.samples)/self.nsamples

class FlatAverageFilter:
    def __init__(self, srcfcn, nsamples, period=0.01):
        self.mutex = threading.RLock()
        self.srcfcn = srcfcn
        self.nsamples = nsamples
        self.samples = []
        self.avg = 0.0
        self.controlLoop = wpilib.Notifier(self.Update)
        self.controlLoop.StartPeriodic(period)

    def Clear(self):
        with self.mutex:
            self.samples = []

    def Update(self):
        with self.mutex:
            self.samples.append(self.srcfcn())
            if len(self.samples) >= self.nsamples:
                self.avg = sum(self.samples)/self.nsamples
                self.samples = []

    def GetAverage(self):
        with self.mutex:
            return self.avg

