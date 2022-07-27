import asyncio

import pyautogui
import websockets
from PySide6.QtCore import QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication


class BenskyMouse:
    def __init__(self):
        self.previousX = 0
        self.previousY = 0

        self.currentX = 0
        self.currentY = 0

        self.mouseDown = 0
        self.mouseDownLength = 0
        self.screen = QApplication.primaryScreen()

    def manageData(self, data):
        if data == "MouseDown":
            self.mouseDown = 1
        elif data == "MouseUp":
            if self.mouseDownLength < 2:
                pyautogui.click()
            self.mouseDownLength = 0
        elif data == "LeftClickPressed":
            pyautogui.mouseDown(button='left')
        elif data == "LeftClickRelease":
            pyautogui.mouseUp(button='left')
            print('LeftRelease')
            print(self.screen.size())
            print(str(QCursor.pos().x()) + " " + str(QCursor.pos().y()))
        elif data == "RightClick":
            pyautogui.click(button='right')
        else:
            self.setMousePosition(data)
            self.mouseDownLength += 1

    def setMousePosition(self, data):
        positions = data.split(":")
        self.currentX = int(float(positions[0]))
        self.currentY = int(float(positions[1]))

        xVariation = (self.currentX - self.previousX)*1.5
        yVariation = (self.currentY - self.previousY)*1.5

        if not self.mouseDown == 0:
            yVariation = 0
            xVariation = 0
            self.mouseDown -= 1

        x = QCursor.pos().x()
        y = QCursor.pos().y()

        if not (x+xVariation < 0) and  not (x+xVariation > self.screen.size().width()-1):
            x += xVariation
        elif x+xVariation<0:
            x = 0
        elif x+xVariation>self.screen.size().width()-1:
            x = self.screen.size().width()-1

        if not (y+yVariation < 0) and  not (y+yVariation > self.screen.size().height()-1):
            y += yVariation
        elif y+yVariation<0:
            y = 0
        elif y+yVariation>self.screen.size().height()-1:
            print("what the hell")
            y = self.screen.size().height()-1
        QCursor.setPos(QPoint(x, y))

        self.previousX = self.currentX
        self.previousY = self.currentY

    async def echo(self, websocket):
        async for message in websocket:
            pos = message.split("/")
            self.manageData(message)

    async def main(self):
        async with websockets.serve(self.echo, "", 8080):
            print("started")
            await asyncio.Future()  # run forever

def runWebsocketServer():
    benskyMouse = BenskyMouse()
    asyncio.run(benskyMouse.main())