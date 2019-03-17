import matplotlib.pyplot as plt
import socketserver
import socket
import re

class Receiver:
    def __init__(self, port=7169, lenght=60):
        plt.ion()
        self.y1 = [0.1 for _ in range(lenght)]
        self.y2 = [0.1 for _ in range(lenght)]
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        self.line1, = ax.plot(self.y1, label='pm2.5')
        self.line2, = ax.plot(self.y2, label='pm10')
        plt.yscale('log')
        plt.ylabel('pm10 in µg/m³')
        plt.ylim(10**-0.2, 1999)
        plt.xlabel('elapsed time in seconds')
        self.L = plt.legend()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host = s.getsockname()[0]
        print(host)
        s.close()
        class TCPHandler(socketserver.BaseRequestHandler):
            def handle(self1):
                self1.data = self1.request.recv(1024).strip()
                self.callback(self1.data.decode())
        self.server = socketserver.TCPServer((host, port), TCPHandler)
        def quitter(*x, **xx):
            self.server.server_close()
        self.fig.canvas.mpl_connect('close_event', quitter)
        self.server.serve_forever()

    def callback(self, data):
        data = re.split(', ', data[1:-1])
        data = [float(i) for i in data]
        print('[INFO] pm2.5: {}  pm10: {}'.format(data[0], data[1]))
        self.L.get_texts()[0].set_text('pm2.5: {} μg/cm³'.format(data[0]))
        self.L.get_texts()[1].set_text('pm10: {}  μg/cm³'.format(data[1]))
        self.y1 = self.y1[:-1]
        self.y1 = [data[0]] + self.y1
        self.line1.set_ydata(self.y1)
        self.y2 = self.y2[:-1]
        self.y2 = [data[1]] + self.y2
        self.line2.set_ydata(self.y2)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

if __name__ == "__main__":
    receiver = Receiver()
