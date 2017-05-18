import subprocess

import time

from client.config import *
import requests
from requests.exceptions import ConnectionError


class Sender():
    def __init__(self):
        pass

    def adsl(self):
        while True:
            (status, output) = subprocess.getstatusoutput(ADSL_BASH)
            if status == 0:
                print('ADSL Successfully')
            try:
                requests.post(SERVER_URL, data={'token': TOKEN, 'port': PROXY_PORT, 'name': CLIENT_NAME})
                print('Successfully Sent to Server', SERVER_URL)
            except ConnectionError:
                print('Failed to Connect Server', SERVER_URL)
            time.sleep(ADSL_CYCLE)


def run():
    sender = Sender()
    sender.adsl()


if __name__ == '__main__':
    run()
