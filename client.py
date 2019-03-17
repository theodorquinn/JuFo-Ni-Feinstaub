from sender import Sender
from reader import Reader

reader = Reader()
sender = Sender()

while True:
    data = reader.read()
    sender.send(data)
