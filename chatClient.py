'''
A simple peer-to-peer chat application

Author: Kyle VanDenHeuvel
'''
import socket, threading, select, re, time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QInputDialog, QSplitter, QMainWindow, QPushButton, QLabel, QTextEdit, QStyle, QStyleFactory
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Setup for GUI
class Application():
    def __init__(self):

        self.q_app = QApplication([])
        ''' Screen Items '''
        # Text window
        self.chat_text = QTextEdit()
        self.chat_text.setStyleSheet("background-color: rgb(44, 47, 51); border-radius: 5px; height: 50px; color: rgb(153, 170, 181); font-size: 14px")
        self.chat_text.setStyle(QStyleFactory.create('Fusion'))
        self.chat_text.setReadOnly(True)
        self.chat_text.insertHtml("<p style=\"text-align: center;\"><strong><span style=\"font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: rgb(153, 170, 181);\">P2P Chat Client</span></strong></p>")
        self.chat_text.insertPlainText("\n")

        # Message terminal
        self.message_term = QTextEdit()
        self.message_term.setStyleSheet("background-color: rgb(44, 47, 51); border-radius: 5px; height: 50px; color: rgb(153, 170, 181); font-size: 14px")
        self.message_term.setReadOnly(False)
        self.message_term.setStyle(QStyleFactory.create('Fusion'))
        self.message_term.setFixedHeight(50)

        # Host Button
        self.host_button = QPushButton("Host")
        self.host_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.host_button.setStyle(QStyleFactory.create('Fusion'))
        self.host_button.setFixedHeight(40)

        # Join Button
        self.join_button = QPushButton("Join")
        self.join_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.join_button.setStyle(QStyleFactory.create('Fusion'))
        self.join_button.setFixedHeight(40)

        # Disconnect Button
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.disconnect_button.setStyle(QStyleFactory.create('Fusion'))
        self.disconnect_button.setFixedHeight(40)

        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.send_button.setStyle(QStyleFactory.create('Fusion'))
        self.send_button.setFixedHeight(40)

        # Clear Chat Button
        self.clear_button = QPushButton("Clear Chat")
        self.clear_button.setStyleSheet("font:bold; color: rgb(153, 170, 181); background-color: rgb(44, 47, 51); font-size: 12px")
        self.clear_button.setStyle(QStyleFactory.create('Fusion'))
        self.clear_button.setFixedHeight(40)

        ''' Layouts '''
        splitV = QSplitter(Qt.Vertical)
        splitH = QSplitter(Qt.Horizontal)

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
        self.window.setStyleSheet("background-color:rgb(35, 39, 42)")
        self.window.resize(640,400)
        self.window.setLayout(main_layout)
        self.window.setWindowTitle("Chat Client")
        self.window.show()


app = Application()
app.q_app.exec_()


