import socket
from threading import Thread, Lock
import variables
import queue


def clientThread(client_id, conn, client_ip, port):
    conn.setblocking(False)
    data = ""
    while True:
        try:
            data += conn.recv(1024).decode()
            # print(data)
        except:
            if not variables.queues_send[client_id].empty():
                send_data = variables.queues_send[client_id].get()
                variables.queues_send[client_id].task_done()
                conn.sendall(send_data.encode())
            continue

        try:
            seperate = data.index("#")
        except ValueError:
            continue

        msg = data[:seperate]
        data = data[seperate+1:]
        variables.queues_recv[client_id].put(msg)

    variables.list_scale_id[client_id] = False
    variables.list_scale_mom[client_id] = "NA"
    conn.close()
    print("connection closed")


def startServer():
    scale_id = 0
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    print('Socket created')

    try:
        soc.bind(("", variables.port_server))

        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    # Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        while True:  # checking for available scale ids
            if variables.list_scale_id[scale_id] == False:
                break
            scale_id += 1
        print('Accepting connection from ' + ip + ':' + port + ' Id is:' + str(scale_id))
        try:

            Thread(target=clientThread, args=(scale_id, conn, ip, port), daemon=True).start()
            variables.list_scale_id[scale_id] = True
            scale_id = 0
        except:
            print("Terrible error!")
            import traceback
            traceback.print_exc()
    soc.close()
