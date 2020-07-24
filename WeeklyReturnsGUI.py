# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QLabel
from PyQt5.QtGui import QIntValidator
from WeeklyStockReturns import *

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        
        # Set Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(762, 620)
        
        
        # Create Central Widget and 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        
        #Create Label for Monte Carlo Image
        self.monte_pic = QtWidgets.QLabel(self.centralwidget)
        self.monte_pic.setGeometry(QtCore.QRect(20, 20, 721, 471))
        self.monte_pic.setText("Graph Appears Here")        
        self.monte_pic.setScaledContents(True)
        self.monte_pic.setObjectName("label")        
    

        # Run Simulation
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 530, 141, 33))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.run_simulation)
        
        
        # Ticker Input Line
        self.ticker_value = ''
        self.ticker_input = QtWidgets.QLineEdit(self.centralwidget)
        self.ticker_input.setGeometry(QtCore.QRect(190, 530, 113, 31))
        self.ticker_input.setObjectName("ticker_input")
        self.ticker_input.editingFinished.connect(self.set_ticker_value)
        
        
        # Start Date Input Line
        self.start_date = ''
        self.start_date_input = QtWidgets.QLineEdit(self.centralwidget)
        self.start_date_input.setGeometry(QtCore.QRect(330, 530, 113, 31))
        self.start_date_input.setObjectName("start_date")
        self.start_date_input.editingFinished.connect(self.set_start_date)
        
        
        # End Date Input Line
        self.end_date = ''
        self.end_date_input = QtWidgets.QLineEdit(self.centralwidget)
        self.end_date_input.setGeometry(QtCore.QRect(470, 530, 113, 31))
        self.end_date_input.setObjectName("end_date")
        self.end_date_input.editingFinished.connect(self.set_end_date)
        
        
        # Labels for Input Lines
        self.ticker_label = QtWidgets.QLabel(self.centralwidget)
        self.ticker_label.setGeometry(QtCore.QRect(195, 500, 113, 31))
        self.ticker_label.setObjectName("ticker_label")
        self.ticker_label.setText("Enter Ticker")      
        
        self.sdate_label = QtWidgets.QLabel(self.centralwidget)
        self.sdate_label.setGeometry(QtCore.QRect(335, 500, 113, 31))
        self.sdate_label.setObjectName("sdate_label")
        self.sdate_label.setText("Start Date")    
        
        self.edate_label = QtWidgets.QLabel(self.centralwidget)
        self.edate_label.setGeometry(QtCore.QRect(475, 500, 113, 31))
        self.edate_label.setObjectName("edate_label")
        self.edate_label.setText("End Date")
        
        self.ticker_example = QtWidgets.QLabel(self.centralwidget)
        self.ticker_example.setGeometry(QtCore.QRect(190, 560, 113, 31))
        self.ticker_example.setObjectName("ticker_example")
        self.ticker_example.setText("Ex: SPY, VTI")
        
        self.date_example = QtWidgets.QLabel(self.centralwidget)
        self.date_example.setGeometry(QtCore.QRect(330, 560, 113, 31))
        self.date_example.setObjectName("date_example")
        self.date_example.setText("Ex: YYYY-MM-DD")
        
        self.date2_example = QtWidgets.QLabel(self.centralwidget)
        self.date2_example.setGeometry(QtCore.QRect(470, 560, 113, 31))
        self.date2_example.setObjectName("date2_example")
        self.date2_example.setText("Ex: YYYY-MM-DD")
        
        # Run retranslatedUi
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Weekly Stock Returns Over Time", "Weekly Stock Returns Over Time"))
        self.pushButton.setText(_translate("Weekly Stock Returns Over Time", "Get Weekly Returns"))


    # Functions to collect simulation data and load the picture
    def run_simulation(self):
        get_Stock_Returns(self.ticker_value, self.start_date, self.end_date)
        self.monte_pic.setPixmap(QtGui.QPixmap("temp_returns.png"))
     
     
    # Functions to accept input for Simulation   
    def set_ticker_value(self):
        self.ticker_value = self.ticker_input.text()
          
    def set_start_date(self):
        self.start_date = self.start_date_input.text()
        
    def set_end_date(self):
        self.end_date = self.end_date_input.text()
        
    def set_years(self):
        self.years = int(self.years_input.text())
    
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
