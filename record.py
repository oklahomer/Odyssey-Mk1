#!/usr/bin/env python
import datetime
from RaspiVidController import *

localtime = datetime.datetime.now()
filename = str(localtime.year) + '_' + str(localtime.month) + '_' + str(localtime.day) + '.h264'

vidcontroller = RaspiVidController(filename, 10000, True)
vidcontroller.start()

vidcontroller.stopController()
