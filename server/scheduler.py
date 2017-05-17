import time
from multiprocessing import Process

import tornado

from server.config import *
from server.receiver import Receiver
from server.tester import Tester


class Scheduler():
    def __init__(self):
        self.tester = Tester()
        self.receiver = Receiver()

    def test(self, ):
        self.tester.run()

    def receive(self):
        self.receiver.run()

    def run(self):


        if RECEIVER_ENABLE:
            receiver_process = Process(target=self.receive)
            receiver_process.start()

        if TESTER_ENABLE:
            tester_process = Process(target=self.test)
            tester_process.start()




