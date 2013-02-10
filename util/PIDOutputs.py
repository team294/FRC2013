import wpilib

class PIDOutputSpeed(wpilib.PIDOutput):
    def __init__(self, output, inv=False):
        super().__init__()
        self.output = output
        self.inv = inv

    def PIDWrite(self, output):
        if self.inv:
            self.output.Set(-output)
        else:
            self.output.Set(output)

