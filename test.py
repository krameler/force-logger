from threading import Thread
import sys
import time
import server
import handler
import variables

import testScale


def calibrate(scale_id):
    if not handler.startCalibration(scale_id):
        print("Couldn't Tar #"+str(scale_id)+"!")
    if not handler.setCalibrationValue(scale_id, "1234"):
        print("Couldn't Calibrate #"+str(scale_id)+"!")


def test(c):
    Thread(target=server.startServer, args=(), daemon=True).start()

    scale = [0, 0, 0, 0, 0, 0]
    for i in range(c):
        scale[i] = Thread(target=testScale.testScale, args=([i]), daemon=True)
        scale[i].start()

    while(not variables.list_scale_id[c-1]):
        pass
    for i in range(c):
        Thread(target=calibrate, args=([i]), daemon=True).start()
    for i in range(c):
        while variables.list_scale_status[i] != variables.STATUS_READY:
            pass

    if not handler.startRecording():
        print("Couldn't start Recording!")
    else:
        time.sleep(1.0)
        handler.stopRecording()

    time.sleep(0.5)
    sys.exit()


test(2)
