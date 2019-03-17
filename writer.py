from reader import Reader
from sys import argv
import os


class Writer:
    def __init__(self, path, port=None):
        if not path.endswith('.csv'):
            path += '.csv'
        self.abspath = os.path.abspath(path)
        if os.path.exists(self.abspath):
            print('[WARNING] continuing with old document')
        else:
            print('[INFO] starting with new document')
        self.reader = Reader(port)

    def run(self):
        while True:
            try:
                with open(self.abspath, 'a') as f:
                    pm25, pm10 = self.reader.read()
                    print('[INFO] pm2.5: {}  pm10: {}, saved at {}'.format(pm25, pm10, self.abspath))
                    f.write(str([pm25, pm10])[1:-1]+'\n')
            except KeyboardInterrupt:
                print('[WARNING] terminated')
                break


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='Messung.csv')
    parser.add_argument('--port', default=None)
    args = parser.parse_args()
    writer = Writer(args.path, args.port)
    writer.run()
