#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GPSController import GPSController
from PiCamController import PiCamController
import time
import sys

class Odyssey():
    def __init__(self):
        # initialize GPSController
        try:
            # it fails when gpsd is not working
            self.gpsController = GPSController()
            self.gpsController.start()

        except:
            exc_info = sys.exc_info()
            print 'Unexpected error on recording: ', exc_info[0], exc_info[1]
            self.gpsController = None

        self.cameraController = PiCamController(self.gpsController)
        self.cameraController.start()

    def datetime(self, format='%Y-%m-%dT%H:%M:%S'):
        if self.gpsController and self.gpsController.utc:
            timeObj = time.strptime(self.gpsController.utc,
                                    '%Y-%m-%dT%H:%M:%S.%fz')
            return time.strftime(format, timeObj)

        else:
            return time.strftime(format, time.gmtime())

    def switch_preview(self):
        if self.cameraController.is_previewing:
            self.cameraController.hide_preview()
        else:
            self.cameraController.show_preview()

    def switch_record(self):
        if (
                self.gpsController
            and self.gpsController.is_logging
            and self.cameraController.recording
        ):
            self.cameraController.stop_recording()
            self.gpsController.stop_logging()

        elif self.cameraController.recording:
            self.cameraController.stop_recording()

        elif self.gpsController and self.gpsController.is_logging:
            self.gpsController.stop_logging()

        else:
            dt = self.datetime('%Y%m%d_%H%M%S')
            self.cameraController.start_recording(dt + '.h264')
            if self.gpsController:
                self.gpsController.start_logging(dt + '.csv')

    def stop(self):
        self.cameraController.stopController()
        if self.gpsController:
            self.gpsController.stopController()

if __name__ == "__main__":
    try:
        import os

        # basic configuration
        os.putenv('SDL_VIDEODRIVER', 'fbcon'                 )
        os.putenv('SDL_FBDEV'      , '/dev/fb1'              )
        os.putenv('SDL_MOUSEDRV'   , 'TSLIB'                 )
        os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

        odyssey = Odyssey()
        odyssey.cameraController.show_preview()
        odyssey.cameraController.start_recording()
        time.sleep(10)

    except KeyboardInterrupt:
        print 'Cancelled'

    except:
        exc_info = sys.exc_info()
        print 'Unexpected error on recording: ', exc_info[0], exc_info[1]

    finally:
        odyssey.stop()
        print 'Done.'
