import os
import subprocess
import threading
import time

RAPIVIDCMD         = ["raspivid"]
TIMETOWAITFORABORT = 0.5

class RaspiVidController(threading.Thread):
    def __init__(self, filePath, timeout, preview, otherOptions=None):
        threading.Thread.__init__(self)

        # prepare raspivid command
        self.raspividcmd = RAPIVIDCMD

        # add options
        self.raspividcmd.append("-o")
        self.raspividcmd.append(filePath)
        self.raspividcmd.append("-t")
        self.raspividcmd.append(str(timeout))
        if preview == False: self.raspividcmd.append("-n")

        # append other options if given
        if otherOptions != None:
            self.raspividcmd = self.raspividcmd + otherOptions

        # set current statement
        self.running = False

    def run(self):
        # start running
        raspivid = subprocess.Popen(self.raspividcmd)

        # loop till its set to stop or it stops
        self.running = True
        while(self.running and raspivid.poll() is None):
            time.sleep(TIMETOWAITFORABORT)
        self.running = False

        if raspivid.poll() == True: raspivid.kill()

    def stopController(self):
        self.running = False
