import datetime
import time
import socket
from urllib import request
from bs4 import BeautifulSoup
import keyboard
import threading
import sys


class EurRubCollector:
    """Class euro/ruble rate collector.
    Parse value of euro/ruble rate ones per given time period from curency exchange stock."""
    url = 'https://www.finanz.ru/valyuty/eur-rub'
    name = 'Euro_Rub exchange rate on stock'

    def __init__(self, time_period, socket):
        self.time = time_period
        self.turned_on = True
        self.current_value = 0
        self.path = str(datetime.date.today()) + '_eur_rub_rate.txt'
        self.sock = socket

    def start_collect(self):
        self.turned_on = True
        while self.turned_on:
            req = request.urlopen(self.url)
            html = req.read()
            soup = BeautifulSoup(html, 'html.parser')
            courses = soup.find_all('div', class_='pricebox content_box')
            for item in courses:
                self.current_value = item.find('th').get_text(strip=True)
                with open(self.path, 'a') as f:
                    f.write(f'Data: {datetime.datetime.now()}, {self.name}: {self.current_value}.\n\n')
            time.sleep(self.time)

    def get_current_state(self):
        return f'Data: {datetime.datetime.now()}, {self.name}: {self.current_value}\n'

    def transmit(self, time_1):
        while True:
            print(f'Data: {datetime.datetime.now()}, {self.name}: {self.current_value}\n')
            self.sock.send(f'Data: {datetime.datetime.now()}, {self.name}: {self.current_value}\n'.encode('utf-8'))
            resp = self.sock.recv(1024)
            print(resp.decode('utf-8'))
            time.sleep(time_1)

    def cleanup(self):
        self.current_value = 0

    def stop_collect(self):
        self.turned_on = False


class MyContextManager:
    """Context manager to open and close socket."""
    def __init__(self):
        self.port = 1976
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.sock.connect(('localhost', self.port))
        print('Connection has been created.')
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


if __name__ == '__main__':
    with MyContextManager() as mcd:
        # Turn collector on
        collector = EurRubCollector(60, mcd)
        thr1 = threading.Thread(target=collector.start_collect)
        thr1.daemon = True
        thr1.start()
        # Turn transmission on
        thr2 = threading.Thread(target=collector.transmit, args=(60,))
        thr2.daemon = True
        thr2.start()

        while True:
            if keyboard.is_pressed('q'):
                print('Execution has been requested to be stopped')
                collector.stop_collect()
                collector.cleanup()
                print('Execution has been stopped')
                sys.exit(-1)
