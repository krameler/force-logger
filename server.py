import socket
from threading import Thread, Lock
import variables
import queue


def clientThread(client_id, conn, client_ip, port):
    conn.setblocking(False)
    data = ""
    while True:
        if not variables.queues_send[client_id].empty():
            send_data = variables.queues_send[client_id].get() + "\n"
            variables.queues_send[client_id].task_done()
            conn.sendall(send_data.encode())
        try:
            data += conn.recv(1024).decode()
            # print(data)
        except:
            continue

        while 42:
            try:
                seperate = data.index("#")
            except ValueError:
                break

            msg = data[:seperate]
            data = data[seperate+1:]

            parts = msg.split(":")
            if msg.count("mes"):
                if variables.en_log == True:
                    variables.list_mes_file[client_id].write(parts[2] + ":" + parts[3] + "\n")
                # print("test")
                variables.list_scale_mom[client_id] = parts[3]
                # print(str(parts[3]))

            elif msg.count("ack"):
                # print("Acknowlege")
                variables.queues_ack[client_id].put(True)

            elif msg.count("blk"):
                if variables.list_blk_file[client_id] != "":
                    variables.list_blk_file[client_id].write(parts[2] + "\n")

            '''
            elif msg.count("ip"):
                list_client_ip[client_id] = msg

            else:
                #print("Wrong command")
                #print(msg)
                msg = None'''

    conn.close()
    print("connection closed")

    # Wait for handler to handle remaining stuff and
    # then clean up and free the id
    variables.list_scale_locks[client_id].acquire()
    variables.lock_lists.acquire()
    variables.queues_send[client_id] = queue.Queue()
    variables.list_scale_mom[client_id] = "NA"
    variables.list_scale_status[client_id] = variables.STATUS_NEW
    variables.list_scale_id[client_id] = False
    variables.lock_lists.release()
    variables.list_scale_locks[client_id].release()


def startServer():
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

        #checking for available scale ids
        variables.lock_lists.acquire()
        try:
            scale_id = variables.list_scale_id.index(False)
        except ValueError:
            print('Connection refused: No available scale_id found!')
            conn.close()
            variables.lock_lists.release()
            continue
        print('Accepting connection from ' + ip + ':' + port + ' Id is:' + str(scale_id))
        try:

            Thread(target=clientThread, args=(scale_id, conn, ip, port), daemon=True).start()
            variables.list_scale_id[scale_id] = True
        except:
            print("Terrible error!")
            import traceback
            traceback.print_exc()
        finally:
            variables.lock_lists.release()
    soc.close()
