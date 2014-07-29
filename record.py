#!/usr/bin/env python
import datetime
import sys
from RaspiVidController import *
from GPSController import *

try:
    localtime   = datetime.datetime.now()
    vidFileName = str(localtime.year) + '_' + str(localtime.month) + '_' + str(localtime.day) + '.h264'
    GPSFileName = str(localtime.year) + '_' + str(localtime.month) + '_' + str(localtime.day) + '.csv'

    vidController = RaspiVidController(vidFileName, 1000 * 60 * 60 * 1, True)
    vidController.start()
    print "start video recording"

    gpsController = GPSController()
    gpsController.start()
    print "start GPS logging"

    GPSFile = open(GPSFileName, 'w')

    while(vidController.isAlive()):
        lat   = gpsController.fix.latitude
        lon   = gpsController.fix.longitude
        speed = gpsController.fix.speed
        utc   = gpsController.utc

        dataString = str(utc) + ',' + str(lat) + ',' + str(lon) + ',' + str(speed) + '\n'
        GPSFile.write(dataString)
        time.sleep(5)

except KeyboardInterrupt:
    print 'Cancelled'

except:
    print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]

finally:
    vidController.stopController()
    gpsController.stopController()
    GPSFile.close()
