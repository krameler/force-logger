from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
 
from untitled import Ui_MainWindow
from threading import Thread, Lock
import sys, socket, queue , time, datetime, os
import server
import handler
import variables
 
class mywindow(QtWidgets.QMainWindow):
 

    
    def __init__(self):
        
        
    
        super(mywindow, self).__init__()
        
        self.ui = Ui_MainWindow()
        
        
        self.ui.setupUi(self)
        
        
        self.qTimer = QTimer()
        self.qTimer.setInterval(1000)
        self.qTimer.timeout.connect(self.updateGui)
        self.qTimer.start()
        
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
    
        Thread(target=server.startServer, args=(), daemon = True).start()
        Thread(target=handler.handlerThread, args=(), daemon = True).start()
        
    def updateGui(self):
        self.ui.ui_lab_value_id0.setText(variables.list_scale_mom[0])
        self.ui.ui_lab_value_id1.setText(variables.list_scale_mom[1])
        self.ui.ui_lab_value_id2.setText(variables.list_scale_mom[2])
        self.ui.ui_lab_value_id3.setText(variables.list_scale_mom[3])
        self.ui.ui_lab_value_id4.setText(variables.list_scale_mom[4])
        self.ui.ui_lab_value_id5.setText(variables.list_scale_mom[5])
        
    def blnk(self, id):
        pass
 
app = QtWidgets.QApplication([])
 
application = mywindow()
 
application.show()
 
sys.exit(app.exec())


    