#!/bin/sh

# Sets basic environmental values here.
## PiTFT output
export SDL_VIDEODRIVER='fbcon'
export SDL_FBDEV='/dev/fb1'
export SDL_MOUSEDRV='TSLIB'
export SDL_MOUSEDEV='/dev/input/touchscreen'
## gpsd
export GPSD_PORT=2947

# PROJECT_ROOT should be determined this way to be used from /etc/init.d/odyssey
PROJECT_ROOT=$(cd `dirname $0` && pwd -P)
sudo -E python $PROJECT_ROOT/record.py
