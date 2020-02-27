from threading import Thread
import socket
import time


def testScale(id):
    def blinker():
        while(blk):
            soc.sendall((":blk:"+str(time.time()-timezero)+":#").encode())
            print("scale"+str(id)+": blk")
            time.sleep(bperiod/1000)

    def measure():
        while(mes):
            stamp = str(time.time()-timezero)
            soc.sendall((":mes:"+stamp+":"+("1"*dec)+":#").encode())
            print("scale"+str(id)+": "+stamp)
            time.sleep(mperiod/1000)

    status = 0
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("127.0.0.1", 4242))
    print("Scale Connected")

    blk = False
    bperiod = 1000
    duration = 500

    mes = False
    factor = 0.5
    weight = 32
    dec = 4
    mperiod = 100
    mcount = 10
    timezero = time.time()

    while(42):
        data = soc.recv(1024).decode()
        cmd = data[:3]
        arg = data[3:]
        print("scale"+str(id)+": " + cmd)
        if status == 0:
            if cmd == "tar":
                mes = 0
            elif cmd == "cal":
                status = 1
            elif cmd == "dec":
                status = 2
            elif cmd == "set":
                factor = 1
            elif cmd == "blk":
                print("Scale blink")
                continue
            elif cmd == "pig":
                blk = not blk
                if blk:
                    Thread(target=blinker, args=(), daemon=True).start()
            elif cmd == "fpn":
                status = 3
            elif cmd == "dpn":
                status = 4
            elif cmd == "fsm":
                status = 5
            elif cmd == "nsm":
                status = 6
            elif cmd == "zer":
                timezero = time.time()
            elif cmd == "poe":
                mes = True
                Thread(target=measure, args=(), daemon=True).start()
            elif cmd == "pod":
                mes = False

        else:
            try:
                arg = int(data)
            except ValueError:
                print("Expected Int!")
                continue
            if status == 1:
                weight = arg
            elif status == 2:
                dec = arg
            elif status == 3:
                bperiod = arg
            elif status == 4:
                duration = arg
            elif status == 5:
                mperiod = arg
            elif status == 6:
                mcount = arg
            status = 0
        soc.sendall("ack#".encode())


if __name__ == '__main__':
    while 42:
        try:
            testScale(0)
        except:
            pass
