import os
import subprocess
import threading
import time

class FrameBufferController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.cmd = os.path.dirname( os.path.abspath( __file__ )) + '/fbcp'

    def run(self):
        fbcp = subprocess.Popen(self.cmd)

        self.running = True
        while self.running:
            pass
        else:
            fbcp.kill()

    def stopController(self):
        self.running = False

if __name__ == '__main__':
    import sys

    try:
        controller = FrameBufferController()
        controller.start()

        print 'Copying framebuffer to /dev/fb1'

        time.sleep(10)

    except KeyboardInterrupt:
        print 'Cancelled'

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]

    finally:
        controller.stopController()
