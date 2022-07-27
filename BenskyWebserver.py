from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

hostName = ""
serverPort = 80


class MyServer(BaseHTTPRequestHandler):
    ipAddress = socket.gethostbyname(socket.gethostname())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(
            '<!DOCTYPE html> <html style="height: 100%;"><head><meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"><title>BenskyMouse</title></head> <body onmousemove="preventScroll()" style="height: 100%;"> '
            '<div id="mouse" ontouchmove="myFunction()" ontouchstart="down()" ontouchend="sendClick(\'MouseUp\')">'

            '</div>'
            '<div id="mouseButtons">'
            '<button id="left" ontouchstart="sendClick(\'LeftClickPressed\')" ontouchend="sendClick(\'LeftClickRelease\')">Left click</button> '
            '<button onclick="sendClick(\'RightClick\')">Right click</button>'
            '</div>'
            '<script> '
            'const websocket = new WebSocket("ws://' + self.ipAddress + ':8080/");'
                                                                        'function preventScroll(){'
                                                                        'event.preventDefault();'
                                                                        '}'
                                                                        'function sendClick(button){'
                                                                        'event.preventDefault();'
                                                                        'websocket.send(button);'
                                                                        '}'
                                                                        'function down(){'
                                                                        'websocket.send("MouseDown");'
                                                                        '} '
                                                                        'function myFunction(){ '
                                                                        'event.preventDefault();'
                                                                        'var xCoords = event.touches[0].clientX; '
                                                                        'var yCoords = event.touches[0].clientY; '
                                                                        'websocket.send(xCoords+":"+yCoords); '
                                                                        '} </script> '
                                                                        '<style>'
                                                                        'body{ margin: 0; } #mouseButtons{ position: fixed; bottom: 0; width: 100%; display: flex; } button{ width: 50%; border: 0; height: 48px; } #left{ border-right: solid 1px white; } #mouse{ background: red; width: 100%; height: 100%; position: absolute; bottom: 49px; }'
                                                                        '</style>'
                                                                        '</body> </html>', "utf-8"))

def runWebServer():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")