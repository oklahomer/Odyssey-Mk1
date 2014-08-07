#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import pygame

import yuv2rgb
import io

yuv = bytearray(320 * 240 * 3 / 2)
rgb = bytearray(320 * 240 * 3)

class PreviewController(threading.Thread):
    def __init__(self, camera, gpsController):
        threading.Thread.__init__(self)

        self.running    = False
        self.is_showing = False

        camera.resolution = self.displaySizeMap[self.displaySize][1]
        camera.rotation   = 180
        camera.crop       = (0.0, 0.0, 1.0, 1.0)
        self.camera = camera

        self.gpsController = gpsController

        # initialize pygame
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    def run(self):
        # start running
        self.running = True
        while self.running:
            if self.is_showing == False:
                continue

            # to store image into in-memory stream
            stream = io.BytesIO()
            self.camera.capture(stream, use_video_port=True, format='raw')
            stream.seek(0)
            stream.readinto(yuv)
            stream.close()

            # convert raw YUV data to RGB
            yuv2rgb.convert(yuv,
                            rgb,
                            self.displaySizeMap[self.displaySize][1][0],
                            self.displaySizeMap[self.displaySize][1][1])

            # fix displaying image
            img = pygame.image.frombuffer(rgb[0:(self.displaySizeMap[self.displaySize][1][0] * self.displaySizeMap[self.displaySize][1][1] * 3)],
                                          self.displaySizeMap[self.displaySize][1],
                                          'RGB')
            self.screen.blit(img,
                             ( (320 - img.get_width() ) / 2,
                               (240 - img.get_height()) / 2) )

            # display recording status
            font = pygame.font.SysFont("freeserif", 18, bold = 1)
            lines = ["Recording : %s" % ('ON' if self.camera.recording else 'OFF')]

            # display speed if GPS receiver is active
            speed = self.gpsController.fix.speed if self.gpsController else None
            if speed:
                lines.append("Speed : %s Km/h" % (speed * 60 * 60 / 1000))
            else:
                lines.append("Speed : N/A")

            marginX = 10
            for line in lines:
                textSurface = font.render(line, 1, pygame.Color(255, 255, 255))
                self.screen.blit(textSurface, (10, marginX))
                marginX += (font.get_linesize() + 5)

            # finally update display
            pygame.display.update()

    def show(self):
        self.is_showing = True

    def hide(self):
        self.screen.fill((0, 0, 0));
        pygame.display.update()
        self.is_showing = False

    def stopController(self):
        self.running = False

    @property
    def displaySize(self):
        # temporarily fixed to 0
        return 0

    @property
    def displaySizeMap(self):
        return [ # Camera parameters for different size settings
                 # Full res     Viewfinder  Crop window
                 [(2592, 1944), (320, 240), (0.0   , 0.0   , 1.0   , 1.0   )], # Large
                 [(1920, 1080), (320, 180), (0.1296, 0.2222, 0.7408, 0.5556)], # Med
                 [(1440, 1080), (320, 240), (0.2222, 0.2222, 0.5556, 0.5556)]  # Small
               ]

if __name__ == '__main__':
    import time
    import sys
    import os

    os.putenv('SDL_VIDEODRIVER', 'fbcon'                 )
    os.putenv('SDL_FBDEV'      , '/dev/fb1'              )
    os.putenv('SDL_MOUSEDRV'   , 'TSLIB'                 )
    os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

    import picamera
    camera = picamera.PiCamera()

    controller = PreviewController(camera, None)
    controller.start()

    try:
        print('Displaying...')
        controller.show()
        time.sleep(5)
        controller.hide()
        time.sleep(5)
        controller.show()
        time.sleep(5)

    except KeyboardInterrupt:
        print 'Cancelled'

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]

    finally:
        controller.stopController()
