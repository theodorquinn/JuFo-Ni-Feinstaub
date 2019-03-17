import socket


class Sender:
    def __init__(self, host='192.168.178.31', port=7169):
        self.host = host
        self.port = port

    def send(self, data):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            sock.sendall(str(data).encode())
            print('[SENT] {}'.format(data))
        except ConnectionRefusedError:
            print('[ERROR] connection refused')


if __name__ == "__main__":
    sender = Sender()
    sender.send('hello world')
