import socket
import sys
import threading

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

import qrcode
from PIL.ImageQt import ImageQt
from BenskyWebserver import runWebServer
from BenskyWebsocketServer import runWebsocketServer

class BenskyMouseGui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bensky Mouse")
        self.setWindowIcon(QIcon("logo.svg"))

        text1 = "Make sure your phone is in the same network of your computer\n"
        text2 = "Or write this link on your browser:"
        text3 = socket.gethostbyname(socket.gethostname()) + '/'

        qr = qrcode.QRCode(version=1, box_size=5, border=0)
        qr.add_data("http://" + text3)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')


        appName = QLabel("Bensky Mouse")
        appNameFont = QFont()
        appNameFont.setPointSize(24)
        appName.setFont(appNameFont)
        appName.setAlignment(Qt.AlignCenter)

        appVersion = QLabel("Version 1.0")
        appVersion.setStyleSheet("color: grey; margin-bottom: 24px")
        appVersion.setAlignment(Qt.AlignCenter)

        message1 = QLabel("Scan this code:")
        message1.setAlignment(Qt.AlignCenter)

        QrCode = QLabel()
        QrCode.setStyleSheet("color: blue; font-size: 20px; margin-bottom: 24px; margin-top: 2px")
        QrCode.setAlignment(Qt.AlignCenter)
        QrCode.setPixmap(QPixmap.fromImage(ImageQt(img)))

        message2 = QLabel("or write this link in your browser:")
        message2.setAlignment(Qt.AlignCenter)

        ipAddress = QLabel(text3)
        ipAddress.setAlignment(Qt.AlignCenter)
        ipAddress.setStyleSheet("color: blue; font-size: 20px; margin-bottom: 24px; margin-top: 2px")

        message3 = QLabel(text1)
        message3.setAlignment(Qt.AlignRight)
        message3.setStyleSheet('color: grey; margin-left: 16px; margin-right: 16px;')

        appInfoLayout = QVBoxLayout()
        appInfoLayout.setAlignment(Qt.AlignCenter)
        appInfoLayout.addWidget(appName)
        appInfoLayout.addWidget(appVersion)
        appInfoLayout.addWidget(message1)
        appInfoLayout.addWidget(QrCode)
        appInfoLayout.addWidget(message2)
        appInfoLayout.addWidget(ipAddress)
        appInfoLayout.addWidget(message3)

        self.setLayout(appInfoLayout)
        self.runServers()

    def runServers(self):
        self.webServer = threading.Thread(target=runWebServer, daemon=True)
        self.webServer.start()

        self.webSocketServer = threading.Thread(target=runWebsocketServer, daemon=True)
        self.webSocketServer.start()

    def closeEvent(self, event):
        super().closeEvent(event)

        sys.exit()

