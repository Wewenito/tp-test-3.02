import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMainWindow, QComboBox, QMessageBox
from PyQt6.QtCore import QCoreApplication, QRect
import time


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.temps_initial = None
        self.valeur = 0

        widget = QWidget()
        self.setCentralWidget(widget)
        self.grid = QGridLayout()
        widget.setLayout(self.grid)

        self.label_top = QLabel("Compteur :")
        self.value = QLabel("0")
        
        self.start = QPushButton("Start")

        self.reset = QPushButton("Reset")
        self.stop = QPushButton("Stop")
        self.connect = QPushButton("Connect")
        self.quit = QPushButton("Quitter")
        

        self.grid.addWidget(self.label_top, 0, 0)
        self.grid.addWidget(self.value, 1, 0)
        self.grid.addWidget(self.start, 2, 0)
        self.grid.addWidget(self.reset, 3, 0)
        self.grid.addWidget(self.stop, 3, 1)
        self.grid.addWidget(self.connect, 4, 0)
        self.grid.addWidget(self.quit, 4, 1)




        self.quit.clicked.connect(self.actionQuitter)

        self.start.clicked.connect(self.actionStart)

        self.reset.clicked.connect(self.actionReset)

    def actionQuitter(self):
        QCoreApplication.exit(0)

    def actionStart(self):
        self.valeur = self.valeur + 1
        print(f"Valeur de start :  {self.valeur}")
        self.value.setText(f"{self.valeur}")

    def actionReset(self):
        self.valeur = 0
        print(f"nouvelle valeur de start : {self.valeur}")
        self.value.setText(f"{self.valeur}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
