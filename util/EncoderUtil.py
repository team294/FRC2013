import wpilib
import math
from DualSpeedController import *
from EncoderSource import EncoderSource
class Encoder294:
    """A special encoder, to keep track of total distance traveled for the odometer and other special things"""
    def __init__(self, digport1, digport2, reversed = False):
        self.encoder = wpilib.Encoder(digport1, digport2, reversed)
        self.totalDistanceTravelled = 0
        self.lastOdoGetDistance = 0
        self.lastRealValue = 0
        self.encoder.Reset()
        
    def Update(self):
        """Call this as often as possible, to get the distance travelled, not displacement."""
        #self.totalDistanceTravelled += abs(self.encoder.Get() - self.totalDistanceTravelled)
        self.totalDistanceTravelled += abs(self.encoder.Get() - self.lastRealValue)
        self.lastRealValue = self.encoder.Get()
    def Reset(self):
        self.encoder.Reset()
        self.lastRealValue = 0
    def Get(self):
        return self.encoder.Get()
    def Start(self):
        self.encoder.Start()
    def PrintOdo(self):
        print(self.totalDistanceTravelled)
    def GetOdo(self):
        return self.totalDistanceTravelled
    def GetChangedSinceLastThisWasCalled(self):
        toReturn = self.totalDistanceTravelled - self.lastOdoGetDistance
        self.lastOdoGetDistance = self.totalDistanceTravelled
        return toReturn
class dualStraightEncoder294(wpilib.PIDSource):
    """For straight ahead and back distance"""
    def __init__(self, lEncoder, rEncoder):
        self.encoderL = lEncoder
        self.encoderR = rEncoder
    def Get(self):
        return (self.encoderL.Get() + self.encoderR.Get())/2
    def Reset(self):
        self.encoderL.Reset()
        self.encoderR.Reset()
    def Start(self):
        self.encoderL.Reset()
        self.encoderR.Reset()
