import datetime
import time
import socket
from urllib import request
from bs4 import BeautifulSoup
import keyboard
import threading
import sys


# Класс сборщик курса евро/рубль на бирже.
class EurRubCollector:
    """Получает раз в заданный период времени значение курса евро/рубль на бирже."""
    url = 'https://www.finanz.ru/valyuty/eur-rub'
    name = 'Euro_Rub exchange rate on stock'

    def __init__(self, time_period):
        self.time = time_period
        self.turned_on = True
        self.current_value = 0
        self.path = str(datetime.date.today()) + '_eur_rub_rate.txt'

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
            sock.send(f'Data: {datetime.datetime.now()}, {self.name}: {self.current_value}\n'.encode('utf-8'))
            resp = sock.recv(1024)
            print(resp.decode('utf-8'))
            time.sleep(time_1)

    def cleanup(self):
        self.current_value = 0

    def stop_collect(self):
        self.turned_on = False


if __name__ == '__main__':
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 1976))
    # Запускаем сборщика
    collector = EurRubCollector(60)
    thr1 = threading.Thread(target=collector.start_collect)
    thr1.daemon = True
    thr1.start()
    # Запускаем передатчика
    thr2 = threading.Thread(target=collector.transmit, args=(60,))
    thr2.daemon = True
    thr2.start()

    while True:
        if keyboard.is_pressed('q'):
            print('Execution has been requested to be stopped')
            collector.stop_collect()
            print('Execution has been stopped')
            sock.close()
            sys.exit(-1)
