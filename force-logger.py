from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel
 
from ui import config_cells, main_window, conf_server_window
from threading import Thread, Lock
import sys, socket, queue , time, datetime, os
import server
import handler
import variables
 
class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.qTimer = QTimer()
        self.qTimer.setInterval(1000)
        self.qTimer.timeout.connect(self.updateGui)
        self.qTimer.start()
        
        self.ui.actionConfLoadcells.triggered.connect(lambda: self.confLoadcells())
        self.ui.actionConfServer.triggered.connect(lambda: self.confServer())
        self.ui.actionConfGraph.triggered.connect(lambda: self.confGraph())
        
        self.ui.ui_but_control_connect.clicked.connect(lambda: Thread(target=server.startServer, args=(), daemon = True).start())
        
        self.ui.ui_lab_unit_id0.setText(variables.list_cell_units[0])
        self.ui.ui_lab_unit_id1.setText(variables.list_cell_units[1])
        self.ui.ui_lab_unit_id2.setText(variables.list_cell_units[2])
        self.ui.ui_lab_unit_id3.setText(variables.list_cell_units[3])
        self.ui.ui_lab_unit_id4.setText(variables.list_cell_units[4])
        self.ui.ui_lab_unit_id5.setText(variables.list_cell_units[5])
        
        self.ui.ui_but_blk_id0.clicked.connect(lambda: self.blnk(0))
        self.ui.ui_but_blk_id1.clicked.connect(lambda: self.blnk(1))
        self.ui.ui_but_blk_id2.clicked.connect(lambda: self.blnk(2))
        self.ui.ui_but_blk_id3.clicked.connect(lambda: self.blnk(3))
        self.ui.ui_but_blk_id4.clicked.connect(lambda: self.blnk(4))
        self.ui.ui_but_blk_id5.clicked.connect(lambda: self.blnk(5))
    
        #Thread(target=server.startServer, args=(), daemon = True).start()
        Thread(target=handler.handlerThread, args=(), daemon = True).start()
        
    def updateGui(self):
        self.ui.ui_lab_value_id0.setText(variables.list_scale_mom[0])
        self.ui.ui_lab_value_id1.setText(variables.list_scale_mom[1])
        self.ui.ui_lab_value_id2.setText(variables.list_scale_mom[2])
        self.ui.ui_lab_value_id3.setText(variables.list_scale_mom[3])
        self.ui.ui_lab_value_id4.setText(variables.list_scale_mom[4])
        self.ui.ui_lab_value_id5.setText(variables.list_scale_mom[5])
        
    def blnk(self, id):
        print("Blinking " + str(id))
        variables.queues_send[id].put("blk\n")
        
    def confLoadcells(self):
        self.SW = windowConfigLoadcells()
        self.SW.show()
        
    def confServer(self):
        self.SW = windowConfigServer()
        self.SW.show()   
        
    def confGraph(self):
        self.SW = windowConfigGraph()
        self.SW.show() 
 
class windowConfigLoadcells(QMainWindow):
    def __init__(self):
        super(windowConfigLoadcells, self).__init__()
        self.ui = config_cells.Ui_conf_cells_window()
        self.ui.setupUi(self)
        
class windowConfigServer(QMainWindow):
    def __init__(self):
        super(windowConfigServer, self).__init__()
        self.ui = conf_server_window.Ui_conf_server_window()
        self.ui.setupUi(self)
        
class windowConfigGraph(QMainWindow):
    def __init__(self):
        super(windowConfigGraph, self).__init__()
        self.ui = config_Graph.Ui_conf_Graph_window()
        self.ui.setupUi(self)
        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())


    