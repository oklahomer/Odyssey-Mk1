import gps
import threading
import time
import sys

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

if __name__ == '__main__':
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
