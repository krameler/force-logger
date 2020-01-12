from datetime import datetime
import os
import variables
import queue


# import main_window

def handlerThread():
    client_id = 0
    client_msg = None

    while True:
        for client_id in range(5):
            # print("looping")
            if variables.list_scale_id[client_id] == True:

                try:
                    client_msg = str(variables.queues_recv[client_id].get(False))
                    variables.queues_recv[client_id].task_done()

                    if client_msg != None:

                        if str(client_msg).count("mes"):
                            parts = client_msg.split(":")
                            if variables.en_log == True:
                                variables.list_mes_file[client_id].write(parts[2] + ":" + parts[3] + "\n")
                            # print("test")
                            variables.list_scale_mom[client_id] = parts[3]
                            print(str(parts[3]))
                            client_msg = ""

                        elif str(client_msg).count("ack"):
                            # print("Acknowlege")
                            variables.queues_ack[client_id].put(True)
                            client_msg = ""
                        '''   
                        elif client_msg.count("ip"):
                            list_client_ip[client_id] = client_msg
                            
                        elif str(client_msg).count("blk"):
                            f = open("log/" + filename + "/" + filename + "_ID" + str(client_id) + ".blk", "a+")
                            f.write(parts[2])
                            f.close()
                        else:
                            #print("Wrong command")
                            #print(client_msg)
                            client_msg = None'''
                except queue.Empty:
                    pass

        client_id = 0
        # time.sleep(0.1)

def startCalibration(client_id):
    if variables.en_log or not variables.list_scale_id[client_id]:
        return False

    variables.queues_send[client_id].put("set")
    variables.queues_ack[client_id].get()
    variables.queues_send[client_id].put("tar")
    variables.queues_ack[client_id].get()
    variables.list_scale_status[client_id] = variables.STATUS_TAR
    return True

def setCalibrationValue(client_id, weight):
    if variables.list_scale_status[client_id] != variables.STATUS_TAR:
        return False

    variables.queues_send[client_id].put("cal")
    variables.queues_ack[client_id].get()
    variables.queues_send[client_id].put(weight)
    variables.queues_ack[client_id].get()
    variables.list_scale_status[client_id] = variables.STATUS_READY
    return True

def startRecording():
    for i in range(6):
        if variables.list_scale_id[i] and variables.list_scale_status[i] != variables.STATUS_READY:
            return False

    timestamp = datetime.now().strftime("%Y.%m.%d_%H-%M-%S")
    os.mkdir(variables.rec_dir + timestamp)
    for i in range(6):
        if variables.list_scale_id[i]:
            variables.list_mes_file[i] = open(variables.rec_dir + timestamp + "/scale" + str(i) + ".log", "w")
            variables.queues_send[i].put("poe")
            variables.queues_ack[i].get()
    variables.en_log = True
    return True

def stopRecording():
    if variables.en_log:
        variables.en_log = False
        for i in range(6):
            if variables.list_scale_id[i]:
                variables.queues_send[i].put("pod")
                variables.list_mes_file[i].close()
                variables.queues_ack[i].get()
