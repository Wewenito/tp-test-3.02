import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMainWindow, QComboBox, QMessageBox
from PyQt6.QtCore import QCoreApplication, QRect
import time
import threading, socket



"""

LE SCRIPT FOURNIT NE MARCHE PAS !

J'ai fait du mieux possible pour cette partie mais sans possibilité de tester reellement le code,

enjoy !


"""


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.temps_initial = None
        self.valeur = 0

        self.arret_thread = False

        self.t = threading.Thread (target=self.__actionStart)

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

        self.thread_no = 0


        self.connect.clicked.connect(self.actionConnect)

        self.quit.clicked.connect(self.actionQuitter)

        self.start.clicked.connect(self.ACTION_START_THREAD)

        self.reset.clicked.connect(self.actionReset)

        self.stop.clicked.connect(self.actionStop)

    def actionQuitter(self):
        if self.client_socket:
            message = "QUIT BUTTON CLICKED"
            self.client_socket.send(message.encode())

        print("Arret du script, on coupe le thread.")
        self.actionStop()
        print("Thread succesfully terminated.")
        time.sleep(3)
        

        QCoreApplication.exit(0)



    #Cette action est celle qui va reellement 'updater' la valeur du chrono.
    # elle va elle même etre declenchee depuis l'event listener qui s'appelle "ACTION_START_THREAD" 
    def __actionStart(self):

        print(self.arret_thread)
        while self.arret_thread == False:
            self.valeur = self.valeur + 1
            print(f"Valeur de start :  {self.valeur}")
            self.value.setText(f"{self.valeur}")
            time.sleep(1)
        else:
            print("chrono has stopped")


    """
        PRESENCE DE L'EXCEPTION POUR LA PARTIE 6 ICI BAS : 
        On ne peut pas reutiliser le meme thread plusieurs fois donc afin d'etre sur
        que cela ne se produise pas, on attend qu'on erreur soit produite si
        la fonction de demarrage du chrono est demarree une 2nd fois.
        Si l'erreur est generee alors on libere completement l'espace memoire reserve au thread,
        puis on le genere de nouveau afin de relancer le chrono de nouveau.
    """

    def ACTION_START_THREAD(self):
        if self.client_socket:
            message = f"START CLICKED, CURRENT VALUE FOR CHRONO : {self.valeur}"
            self.client_socket.send(message.encode())



        print("starting thread")
        try:
            self.arret_thread = False
            self.t.start()
        except Exception as e:
            print("ERROR, Not first thread created..")
            self.t = None

            self.t = threading.Thread (target=self.__actionStart)
            self.t.start()





    #Cette action revient a prendre la valeur globale du chrono et a la ramener a sa valeur de depart (0)
    def actionReset(self):
        if self.client_socket:
            message = "RESET CLICKED"
            self.client_socket.send(message.encode())


        self.valeur = 0
        print(f"nouvelle valeur de start : {self.valeur}")
        self.value.setText(f"{self.valeur}")


    #Cette action passe simplement le booleen de false a true pour arreter le comptage.
    #on attend ensuite la conclusion logique du thread.
    def actionStop(self):
        if self.client_socket:
            message = "bye"
            self.client_socket.send(message.encode())
        print("STOP")
        self.arret_thread = True
        self.t.join()


    def actionConnect(self):
        self.client_socket = socket.socket()

        try:
            self.client_socket.connect(("127.0.0.1", 10000))
            print("Success connecting to server")
        except ConnectionRefusedError as error:
            print("Error connecting to the server")
            print(error)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
