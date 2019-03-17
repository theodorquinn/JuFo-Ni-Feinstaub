import matplotlib.pyplot as plt
from reader import Reader


class Grapher:
    def __init__(self, lenght=60):
        plt.ion()
        self.reader = Reader()
        self.lenght = lenght
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
        while True:
            self.callback()

    def callback(self):
        data = self.reader.read()
        print('[INFO] pm2.5: {}  pm10: {}'.format(data[0], data[1]))
        self.L.get_texts()[0].set_text('pm2.5: {} μg/cm³'.format(data[0]))
        self.L.get_texts()[1].set_text('pm10:  {} μg/cm³'.format(data[1]))
        self.y1 = self.y1[:-1]
        self.y1 = [data[0]] + self.y1
        self.line1.set_ydata(self.y1)
        self.y2 = self.y2[:-1]
        self.y2 = [data[1]] + self.y2
        self.line2.set_ydata(self.y2)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


if __name__ == "__main__":
    grapher = Grapher()