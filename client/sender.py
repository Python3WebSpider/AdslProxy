import subprocess

import time

from client.config import *
import requests


class Sender():
    def __init__(self):
        pass

    def adsl(self):
        while True:
            (status, output) = subprocess.getstatusoutput(ADSL_BASH)
            print(status)
            if status == 0:
                print('ADSL Successfully')
            print(output)
            requests.post(SERVER_URL, data={'token': TOKEN, 'port': PROXY_PORT})
            time.sleep(ADSL_CYCLE)


def run():
    sender = Sender()
    sender.adsl_start()


if __name__ == '__main__':
    run()
