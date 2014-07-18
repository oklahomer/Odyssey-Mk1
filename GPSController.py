import gps
import threading

class GPSController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps.gps("localhost", "2947")
        self.gpsd.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        # set current statement
        self.running = False

    def run(self):
        # start running
        self.running = True
        while self.running:
            self.gpsd.next()

    def stopController(self):
        self.running = False

    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        return self.gpsd.utc
