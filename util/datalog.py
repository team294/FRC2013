import threading
import time
import socket
import struct
import wpilib

LogIP = "10.2.94.125"

class DataLogger(threading.Thread):
    def __init__(self, getfcn, period, port):
        super().__init__()
        self.getfcn = getfcn
        self.period = period
        self.port = port

    def run(self):
        return
        if not wpilib.Preferences.GetInstance().GetBoolean("ProductionMode"):
            print("Starting DataLogger to %s port %d" % (LogIP, self.port))
            HOST, PORT = LogIP, self.port
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while True:
                sock.sendto(self.getfcn(), (HOST, PORT))
                time.sleep(self.period)

def LogData(getfcn, period, port):
    datalogger = DataLogger(getfcn, period, port)
    datalogger.start()
    return datalogger

class LoggingPIDController(wpilib.PIDController):
    data_struct = struct.Struct("<ddddddd")
    data_struct2 = struct.Struct("<dddddddd")

    def __init__(self, p, i, d, source, output, period=0.05, port=8888):
        super().__init__(p, i, d, source, output, period)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port

    def CalculateCallback(self, input, setpoint, result, error):
        return
        if wpilib.Preferences.GetInstance().GetBoolean("ProductionMode"):
            return
        if self.sock is None:
            return
        with self.semaphore:
            P = self.P
            I = self.I
            D = self.D
        curspeed = getattr(self.pidOutput, "curspeed", None)
        if curspeed is not None:
            data = self.data_struct2.pack(P, I, D, input, setpoint, result, error, curspeed)
        else:
            data = self.data_struct.pack(P, I, D, input, setpoint, result, error)
        try:
            self.sock.sendto(data, (LogIP, self.port))
        except socket.error:
            self.sock = None

class LoggingPIDController254(wpilib.PIDController):
    def __init__(self, p, i, d, source, output, period=0.05, port=41234):
        super().__init__(p, i, d, source, output, period)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port

    def CalculateCallback(self, input, setpoint, result, error):
        if wpilib.Preferences.GetInstance().GetBoolean("ProductionMode"):
            return
        if self.sock is None:
            return
        data = '{"S":%f, "V":%f, "C":%f}' % (setpoint, input, result)
        try:
            self.sock.sendto(data.encode(), (LogIP, self.port))
        except socket.error:
            self.sock = None
