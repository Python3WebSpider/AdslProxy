import subprocess


class Sender():
    def __init__(self):
        pass

    def adsl_start(self):
        (status, output) = subprocess.getstatusoutput('pwd')
        print(status)
        print(output)


def run():
    sender = Sender()
    sender.adsl_start()


if __name__ == '__main__':
    run()