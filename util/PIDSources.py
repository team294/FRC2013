import wpilib

class PIDSourcePot(wpilib.PIDSource):
    def __init__(self, pot):
        super().__init__()
        self.pot = pot

    def PIDGet(self):
        val = self.pot.GetAverageValue()
        if val < 0:
            return None
        return val

class PIDSourceEncoder(wpilib.PIDSource):
    def __init__(self, encoder, zero=0, scale=1.0):
        super().__init__()
        self.encoder = encoder
        self.zero = zero
        self.scale = scale

    def PIDGet(self):
        return (self.encoder.Get()+self.zero)*self.scale
