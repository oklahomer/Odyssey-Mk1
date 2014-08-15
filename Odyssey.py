#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GPSController import GPSController
from PreviewController import PreviewController
import picamera
import sys

class Odyssey():
    def __init__(self):
        # initialize GPSController
        try:
            self.gpsController = GPSController()
            self.gpsController.start()

        except:
            exc_info = sys.exc_info()
            print 'Unexpected error on recording: ', exc_info[0], exc_info[1]
            self.gpsController = None

        # inititialize camera
        camera = picamera.PiCamera()
        camera.resolution = (1024, 768)
        camera.rotation   = 180
        camera.crop       = (0.0, 0.0, 1.0, 1.0)

        self.camera = camera
        self.previewController = PreviewController(self.camera,
                                                   self.gpsController)
        self.previewController.start()

    def show_preview(self):
        self.previewController.show()

    def hide_preview(self):
        self.previewController.hide()

    def switch_preview(self):
        if self.previewController.is_showing:
            self.hide_preview()
        else:
            self.show_preview()

    def start_recording(self):
        # should set inline_headers to deal w/ older firmware
        # https://github.com/waveform80/picamera/issues/33
        if not self.camera.recording:
            self.camera.start_recording('vid.h264', format='h264', inline_headers=False)

    def stop_recording(self):
        if self.camera.recording:
            self.camera.stop_recording()

    def switch_record(self):
        if self.camera.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def stop(self):
        self.stop_recording()
        self.previewController.stopController()
        self.camera.close()
        if self.gpsController:
            self.gpsController.stopController()

if __name__ == "__main__":
    try:
        import os
        import time

        # basic configuration
        os.putenv('SDL_VIDEODRIVER', 'fbcon'                 )
        os.putenv('SDL_FBDEV'      , '/dev/fb1'              )
        os.putenv('SDL_MOUSEDRV'   , 'TSLIB'                 )
        os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

        odyssey = Odyssey()
        odyssey.show_preview()
        odyssey.start_recording()
        time.sleep(10)

    except KeyboardInterrupt:
        print 'Cancelled'

    except:
        exc_info = sys.exc_info()
        print 'Unexpected error on recording: ', exc_info[0], exc_info[1]

    finally:
        odyssey.stop()
        print 'Done.'
