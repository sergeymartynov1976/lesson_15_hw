import datetime
#import time
import socket


class MyContextManager:
    """Context manager to open and close socket."""
    def __init__(self):
        self.port = 1976
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', self.port))
        self.sock.listen(1)
        print('Socket has been created.')
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


# Processing connections
with MyContextManager() as mcd:
    while True:
        client, addr = mcd.accept()
        print('Connected: ', addr)

        while True:
            data = client.recv(1024 )
            if not data:
                break
            udata = data.decode('utf-8')
            with open('transmission.txt', 'a') as f:
                f.write(udata)
                f.write('**' * 50 + '\n')
            client.send(f'{datetime.datetime.now()} - Data received'.encode('utf-8'))
            print(f'Transmission completed at: {datetime.datetime.now()}')

