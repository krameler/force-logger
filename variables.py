import queue
from threading import Thread, Lock

en_log = False
en_blink = False

list_scale_id = [False, False, False, False, False]
list_client_ip = ["NC", "NC" , "NC", "NC", "NC"]
list_cell_units = ["", "", "", "", "", ""]
list_scale_mom = ["", "", "", "", "", ""]
port_server=4242

queues_recv =[]
for i in range(5):
    queues_recv.append(queue.Queue())
    
queues_send =[]
for i in range(5):
    queues_send.append(queue.Queue())
    
queues_ack = []
for i in range(5):
    queues_ack.append(queue.Queue())
    
queues_mes = []
for i in range(5):
    queues_mes.append(queue.LifoQueue())
    
lock_file_mes = []
for i in range(5):
    lock = Lock()
    lock_file_mes.append(lock)