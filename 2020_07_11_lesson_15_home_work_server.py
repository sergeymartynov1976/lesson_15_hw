import datetime
#import time
import socket


# Create socket
sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)

sock.bind(('localhost', 1976))
sock.listen(1)


# Processing connections
while True:
    client, addr = sock.accept()
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

    client.close()
