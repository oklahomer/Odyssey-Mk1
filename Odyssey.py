#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GPSController import GPSController
from PreviewController import PreviewController
import picamera
import pygame
import yuv2rgb
import io
import os

class Odyssey():
    def __init__(self):
        # initialize GPSController
        self.gpsController = GPSController()
        self.gpsController.start()

        # inititialize camera and display
        self.camera = picamera.PiCamera()
        self.previewController = PreviewController(self.camera,
                                                   self.gpsController)

        # initialize pygame
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    def show_preview(self):
        self.previewController.start()

    def start_recording(self):
        # should set inline_headers to deal w/ older firmware
        # https://github.com/waveform80/picamera/issues/33
        if self.camera.recording == False:
            self.camera.start_recording('vid.h264', inline_headers=False)

    def stop_recording(self):
        if self.camera.recording == True:
            self.camera.stop_recording()

if __name__ == "__main__":
    try:
        import os
        import sys
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
        odyssey.stop_recording()
        odyssey.previewController.stopController()
        odyssey.gpsController.stopController()
        odyssey.camera.close()
        print 'Done.'
