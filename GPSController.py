import gps
import threading
import time

class GPSController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps.gps("localhost", "2947")
        self.gpsd.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        self.file = None

        # set current statement
        self.running        = False
        self.is_logging     = False
        self.lastLoggedTime = None

    def run(self):
        # start running
        self.running = True
        while self.running:
            self.gpsd.next()

            if self.is_logging and self.file:
                currentTime = time.time()
                if self.lastLoggedTime:
                    if currentTime - self.lastLoggedTime < 5:
                        continue

                lat   = self.fix.latitude
                lon   = self.fix.longitude
                speed = self.fix.speed
                utf   = self.utc
                dataString = self.utc   + ',' + str(lat) + ',' + str(lon)  + ',' + str(speed) + '\n'

                self.file.write(dataString)
                self.lastLoggedTime = currentTime

    def stopController(self):
        self.running = False
        if self.file:
            self.file.close()

    def start_logging(self, fileName='gps_log.csv'):
        self.file       = open(fileName, 'w')
        self.is_logging = True

    def stop_logging(self):
        self.is_logging = False
        if self.file:
            self.file.close()

    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        # self.gpsd.fix.time can be either float or an ISO8601 string
        # Use self.gpsd.utc, instead.
        return self.gpsd.utc

if __name__ == '__main__':
    import sys

    gpsController = GPSController()

    try:
        print('Locating...')

        gpsController.start()

        while (gpsController.isAlive()):
            lat   = gpsController.fix.latitude
            lon   = gpsController.fix.longitude
            speed = gpsController.fix.speed
            utc   = gpsController.utc

            dataString = str(utc) + ',' + str(lat) + ',' + str(lon) + ',' + str(speed)
            print(dataString)

            time.sleep(3)

    except KeyboardInterrupt:
        print 'Cancelled'

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]

    finally:
        gpsController.stopController()
