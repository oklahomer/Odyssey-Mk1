#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import pygame
import time
import io
import picamera

class PiCamController(threading.Thread):
    def __init__(self, gpsController=None):
        threading.Thread.__init__(self)

        # initialize camera
        camera = picamera.PiCamera()
        camera.resolution = (1024, 768)
        camera.rotation   = 180
        camera.crop       = (0.0, 0.0, 1.0, 1.0)
        self.camera       = camera

        self.gpsController = gpsController

        # initialize pygame
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        self.rgb = bytearray(
            camera.resolution[0] * camera.resolution[1] * 3
            )

        # set current statement
        self.running       = False
        self.is_previewing = False

    def run(self):
        # start running
        self.running = True
        while self.running:
            if not self.is_previewing:
                continue

            # to store image into in-memory stream
            stream = io.BytesIO()
            self.camera.capture(
                stream, use_video_port=True, format='rgb', resize=(320, 240)
                )
            stream.seek(0)
            stream.readinto(self.rgb)
            stream.close()

            # fix displaying image
            img = pygame.image.frombuffer(
                self.rgb[0:(320 * 240 * 3)], (320, 240), 'RGB'
                )
            self.screen.blit(img, (0, 0))

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

    def show_preview(self):
        self.is_previewing = True

    def hide_preview(self):
        # tell run() NOT to refresh screen any more
        # and wait till it actually stops
        self.is_previewing = False
        time.sleep(0.3)

        # then show black screen
        self.screen.fill((0, 0, 0));
        pygame.display.update()

    def start_recording(self, fileName='vid.h264'):
        if not self.camera.recording:
            # should set inline_headers to deal w/ older firmware
            # https://github.com/waveform80/picamera/issues/33
            self.camera.start_recording(fileName, format='h264', inline_headers=False)

    def stop_recording(self):
        if self.camera.recording:
            self.camera.stop_recording()

    def stopController(self):
        self.running = False
        self.stop_recording()
        self.camera.close()

    @property
    def recording(self):
        return self.camera.recording

if __name__ == '__main__':
    import sys
    import os

    os.putenv('SDL_VIDEODRIVER', 'fbcon'                 )
    os.putenv('SDL_FBDEV'      , '/dev/fb1'              )
    os.putenv('SDL_MOUSEDRV'   , 'TSLIB'                 )
    os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

    try:
        controller = PiCamController()
        controller.start()

        print('Displaying...')
        controller.show_preview()
        time.sleep(5)
        controller.hide_preview()
        time.sleep(5)
        controller.show_preview()
        time.sleep(5)

    except KeyboardInterrupt:
        print 'Cancelled'

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]

    finally:
        controller.stopController()
