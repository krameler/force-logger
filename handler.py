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
                                lock_file_mes[client_id].acquire()
                                f = open("log/" + filename + "/" + filename + "_ID" + str(client_id) + ".log", "a+")
                                f.write(parts[2] + ":" + parts[3] + "\n")
                                f.close()
                                lock_file_mes[client_id].release()
                                # print("writing to file")
                            print("test")
                            variables.list_scale_mom[client_id] = parts[3]
                            print(str(parts[3]))
                            client_msg = ""

                        elif str(client_msg).count("ack"):
                            print("Acknowlege")
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
