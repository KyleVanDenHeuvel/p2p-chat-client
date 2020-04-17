'''
A simple peer-to-peer chat application

Author: Kyle VanDenHeuvel
'''
import socket, threading, select, re, time, sys, traceback
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QDialog, QInputDialog, QSplitter, QMainWindow, QPushButton, QLabel, QTextEdit, QLineEdit, QStyle, QStyleFactory
from PyQt5.QtCore import Qt, QThread, pyqtSignal


# A class to assist in sending messages
class mess_text(QLineEdit):
    def __init__(self, callback):
        self.enter_callback = callback
        super().__init__()


# Overwrites a method in QThread
class Listener(QThread):
    signal = pyqtSignal(object)

    def __init__(self, socket):
        QThread.__init__(self)
        self.socket = socket
    
    def run(self):
        with self.socket:
            while(True):
                try:
                    message = self.socket.recv(32000).decode()
                except:
                    self.socket.close()
                    traceback.print_exc(file=sys.stdout)
                    return
                if message == "<<<END CONNECTION>>>":
                    self.socket.sendall("<<<END CONNECTION>>>".encode())
                    self.socket.close()
                    break
                self.signal.emit(message)
        print("Connection has been closed")


# Setup for GUI
class Application():
    def __init__(self):

        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.q_app = QApplication([])


        ''' Screen Items '''
        # Text window
        self.chat_text = QTextEdit()
        self.chat_text.setStyleSheet("background-color: rgb(44, 47, 51); border-radius: 5px; height: 50px; color: rgb(153, 170, 181); font-size: 14px")
        self.chat_text.setStyle(QStyleFactory.create('Fusion'))
        self.chat_text.setReadOnly(True)
        self.chat_text.insertPlainText("\n")

        # Message terminal
        self.message_term = mess_text(self.send_mes)
        self.message_term.setStyleSheet("background-color: rgb(44, 47, 51); border-radius: 5px; height: 50px; color: rgb(153, 170, 181); font-size: 14px")
        self.message_term.setReadOnly(False)
        self.message_term.setStyle(QStyleFactory.create('Fusion'))
        self.message_term.setFixedHeight(50)

        # Chat Status
        self.chat_status = QTextEdit()
        self.chat_status.setStyleSheet("background-color: rgb(44, 47, 51); border-radius: 5px; height: 50px; color: rgb(153, 170, 181); font-size: 14px")
        self.chat_status.setReadOnly(True)
        self.chat_status.setStyle(QStyleFactory.create('Fusion'))
        self.chat_status.insertHtml("<p style=\"text-align: center;\"><strong><span style=\"font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: rgb(153, 170, 181);\">Connect or Host</span></strong></p>")
        self.chat_status.setFixedHeight(30)

        # Host Button
        self.host_button = QPushButton("Host")
        self.host_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.host_button.setStyle(QStyleFactory.create('Fusion'))
        self.host_button.setFixedHeight(40)
        self.host_button.clicked.connect(self.host)

        # Join Button
        self.join_button = QPushButton("Join")
        self.join_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.join_button.setStyle(QStyleFactory.create('Fusion'))
        self.join_button.setFixedHeight(40)
        self.join_button.clicked.connect(self.join)

        # Disconnect Button
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.disconnect_button.setStyle(QStyleFactory.create('Fusion'))
        self.disconnect_button.setFixedHeight(40)
        self.disconnect_button.clicked.connect(self.disconnect)

        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.send_button.setStyle(QStyleFactory.create('Fusion'))
        self.send_button.setFixedHeight(50)
        self.send_button.clicked.connect(self.send_mes)

        # Clear Chat Button
        self.clear_button = QPushButton("Clear Chat")
        self.clear_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.clear_button.setStyle(QStyleFactory.create('Fusion'))
        self.clear_button.setFixedHeight(40)
        self.clear_button.clicked.connect(self.clear_chat)


        ''' Layouts '''

        splitV = QSplitter(Qt.Vertical)     # Vertical splitter
        splitH = QSplitter(Qt.Horizontal)   # Horizontal splitter

        # Chat Layout
        chat_layout = QVBoxLayout()
        chat_layout.addWidget(self.host_button)
        chat_layout.addWidget(self.join_button)
        chat_layout.addWidget(self.disconnect_button)
        chat_layout.addWidget(self.clear_button)
        chat_layout.addWidget(splitV)
        chat_layout.addWidget(self.send_button)
        chat_layout.setSpacing(15)

        # Message Layout
        mes_layout = QVBoxLayout()
        mes_layout.addWidget(self.chat_status)
        mes_layout.addWidget(splitH)
        mes_layout.addWidget(self.chat_text)
        mes_layout.addWidget(splitH)
        mes_layout.addWidget(self.message_term)

        # Primary Layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(chat_layout)
        main_layout.addWidget(splitV)
        main_layout.addLayout(mes_layout)

        # Window
        self.window = QWidget()
        self.window.setStyle(QStyleFactory.create('Fusion'))
        self.window.setStyleSheet("color: rgb(153, 170, 181);background-color:rgb(35, 39, 42)")
        self.window.resize(640,400)
        self.window.setLayout(main_layout)
        self.window.setWindowTitle("Chat Client")
        self.window.show()


    '''Application Functions'''

    # Function to set up a connection
    def host(self):

        # Prompt user to set port number
        port_num, status = QInputDialog().getText(self.window, "Host", "Provide a port number between 1024 and 65535", QLineEdit.Normal)

        # Error checking for port number
        if status and (not port_num.isdigit() or not (int(port_num)) in range(1023, 65536)):
            self.host()
        if status and port_num:
            self.connected = True

            try:

                # Prompt waiting for other user
                self.chat_status.setText("Waiting for connection")

                # Starting server
                self.socket.bind(("0.0.0.0", int(port_num)))
                self.socket.listen()
                other, client = self.socket.accept()
                self.socket.close()
                self.socket = other

                # Message for established connection
                self.chat_status.setText("Established connection with " + str(client))

                # Listening
                self.listen = Listener(other)
                self.listen.start()
                self.listen.finished.connect(self.close_connection)
                self.listen.signal.connect(self.create_mes)

            except:
                self.connected = False
                connect_error = QMessageBox()
                connect_error.setText("Something went wrong.  Please try again")
                connect_error.setStyle(QStyleFactory.create("Fusion"))
                connect_error.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
                connect_error.exec()
                traceback.print_exc(file=sys.stdout)
               

    # Function to join an open connection
    def join(self):
        
        host_ip, status = QInputDialog().getText(self.window, "Join", "Provide IP and Port (format: IP:port)", QLineEdit.Normal)
        host_info = host_ip.split(':')

        # Checks to see if port is included, and if it is, if it is a number
        if status and not (len(host_info) == 2 and host_info[1].isdigit()):
            self.join()

        # Checks to ensure proper IP address format
        elif status:
            try:
                socket.inet_aton(host_info[0])
            except socket.error:
                self.join()

        # Checks to ensure the port is within proper range
        elif status and not (len(host_info) == 2 and (1024 <= host_info[1] <= 65535)):
            self.join()

        # If formatted correctly, attempt to connect
        if status and host_ip:

            try:
                # Attempt to connect to other client
                self.socket.connect((host_info[0], int(host_info[1])))
                self.chat_status.setText("Connected to " + host_info[0])

                self.connected = True

                # Listening
                self.listen = Listener(self.socket)
                self.listen.start()
                self.listen.finished.connect(self.close_connection)
                self.listen.signal.connect(self.create_mes)

            except Exception:
                bad_connect = QMessageBox()
                bad_connect.setText("Please first establish a connection")
                bad_connect.setStyle(QStyleFactory.create("Fusion"))
                bad_connect.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
                bad_connect.exec()
                self.chat_status.setText("")
                self.chat_status.insertHtml("<p style=\"text-align: center;\"><strong><span style=\"font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: rgb(153, 170, 181);\">Connect or Host</span></strong></p>")
                traceback.print_exc(file=sys.stdout)


    # Function to disconnect from current session
    def disconnect(self):
        # check to see if connection is established
        if self.connected:
            self.socket.sendall("<<<END CONNECTION>>>".encode())
        else:
            bad_connect = QMessageBox()
            bad_connect.setText("Please first establish a connection")
            bad_connect.setStyle(QStyleFactory.create("Fusion"))
            bad_connect.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
            bad_connect.exec()


    # Function that brings application back to unconnected state
    def close_connection(self):
        self.chat_status.insertHtml("<p style=\"text-align: center;\"><strong><span style=\"font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: rgb(153, 170, 181);\">Closing connection</span></strong></p>")
        self.socket.close()
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_status.setText("<p style=\"text-align: center;\"><strong><span style=\"font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: rgb(153, 170, 181);\">Connect or Host</span></strong></p>")


    # Function to create a message
    def create_mes(self, message):
        self.chat_text.insertHtml(message)
        self.chat_text.insertPlainText("\n")


    # Function to send a message
    def send_mes(self):
        # Check to see if connection is established
        if self.connected:
            # Send user message to chat window
            self.chat_text.insertHtml("<b>Me: </b>" + self.message_term.text())
            self.chat_text.insertPlainText("\n")

            # Send message across client
            self.socket.sendall(("<b>Person: </b>" + self.message_term.text()).encode())

            # Clear message terminal
            self.message_term.setText("")
        else:
            bad_connect = QMessageBox()
            bad_connect.setText("Please first establish a connection")
            bad_connect.setStyle(QStyleFactory.create("Fusion"))
            bad_connect.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
            bad_connect.exec()


    # Function to clear the chat window
    def clear_chat(self):
        # Check to see if connection is established
        if self.connected:
            self.chat_text.setText(" ")
        else:
            bad_connect = QMessageBox()
            bad_connect.setText("Please first establish a connection")
            bad_connect.setStyle(QStyleFactory.create("Fusion"))
            bad_connect.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
            bad_connect.exec()


# Start Application
app = Application()
app.q_app.exec_()   
app.socket.close()  