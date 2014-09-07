#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import picamera
from PIL import Image, ImageDraw, ImageFont

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

        # set current statement
        self.running        = False
        self.status_overlay = None

    def run(self):
        # start running
        self.running = True
        while self.running:
            if self.camera.previewing: self.refresh_status_overlay()

    def refresh_status_overlay(self):

        text_array = []

        # add recording status
        text_array.append('Recording : %s' % ('ON' if self.camera.recording else 'OFF'))

        # add driving speed
        speed = (str(self.gpsController.fix.speed * 60 * 60 / 1000) + 'Km/h'
                    if self.gpsController and self.gpsController.fix.speed
                    else 'N/A')
        text_array.append('Speed : %s' % speed)

        # prepare image to be overlayed
        img = Image.new('RGB', self.camera.resolution)
        draw = ImageDraw.Draw(img)
        draw.font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 75)

        top_margin = 5
        for text in text_array:
            draw.text((5, top_margin), text, fill=(255, 255, 255))
            top_margin += draw.font.getsize(text)[1] + 5

        if not self.status_overlay:
            self.status_overlay = self.camera.add_overlay(
                img.tostring(), layer=5, size=img.size, alpha=128)
        else:
            self.status_overlay.update(img.tostring())

    def show_preview(self):
        self.camera.start_preview()

    def hide_preview(self):
        self.camera.stop_preview()
        if self.status_overlay:
            self.camera.remove_overlay(self.status_overlay)

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
    import time

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
