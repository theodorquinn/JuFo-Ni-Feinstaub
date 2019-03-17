import serial
import struct
import os


class Reader:
    def __init__(self, port=None):
        self.ser = self.connect(port)

    def read(self):
        ''' returns list of [pm2.5µ, pm10µ]'''
        byte = 0
        while str(byte)[3:-1] != 'xaa':
            byte = self.ser.read(size=1)
        message = byte + self.ser.read(size=10)
        decoded = struct.unpack('<HHxxBBB', message[2:])
        pm25 = decoded[0]/10
        pm10 = decoded[1]/10
        return [pm25, pm10]

    def show(self):
        while True:
            try:
                pm25, pm10 = self.read()
                print('[INFO] pm2.5: {}  pm10: {}'.format(pm25, pm10))
            except KeyboardInterrupt:
                print('[WARNING] terminated')
                break

    def connect(self, port=None):
        ser = None
        if port is None:
            if os.name == 'nt':
                print('[OK] running on windows')
                for i in range(16):
                    try:
                        ser = serial.Serial('COM{}'.format(i), 9600)
                        print('[OK] sensor connected at COM{}'.format(i))
                        break
                    except:
                        pass
            else:
                print('[OK] running on rasperry')
                for i in range(4):
                    try:
                        ser = serial.Serial('/dev/ttyUSB{}'.format(i), 9600)
                        print('[OK] sensor connected at /dev/ttyUSB{}'.format(i))
                        break
                    except:
                        pass
            if ser is None:
                raise RuntimeError('no sensor found')
        else:
            try:
                ser = serial.Serial(port, 9600)
            except:
                pass
        return ser


if __name__ == '__main__':
    reader = Reader()
    reader.show()
