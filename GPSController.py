import gps
import threading
import time
import subprocess
import os

class GPSController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        gpsdPort = os.getenv('GPSD_PORT', 2947)

        subprocess.call('pkill gpsd', shell=True)
        subprocess.call(
            'gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock -S %d' % gpsdPort,
            shell=True)

        self.gpsd = gps.gps("localhost", gpsdPort)
        self.gpsd.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        self.file = None
        self.fileName = None

        # set current statement
        self.running        = False
        self.is_logging     = False
        self.lastLoggedTime = None

    def run(self):
        # start running
        self.running = True

        while self.running:
            self.gpsd.next()

            if self.is_logging:
                currentTime = time.time()

                if (not self.lastLoggedTime
                    or currentTime - self.lastLoggedTime >= 5):

                    self.writeLog()
                    self.lastLoggedTime = currentTime

    def writeLog(self):
        dataString = ','.join([self.utc,
                               str(self.fix.latitude),
                               str(self.fix.longitude),
                               str(self.fix.speed)]
                               )

        file = open(self.fileName, 'a')
        file.write(dataString + '\n')
        file.close()

    def stopController(self):
        self.running = False

    def start_logging(self, fileName='gps_log.csv'):
        self.fileName   = fileName
        self.is_logging = True

    def stop_logging(self):
        self.is_logging = False

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

            dataString = ','.join([utc, str(lat), str(lon), str(speed)])
            print(dataString)

            time.sleep(3)

    except KeyboardInterrupt:
        print 'Cancelled'

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]

    finally:
        gpsController.stopController()
