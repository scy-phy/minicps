import subprocess
from time import sleep


class Pinger:
    NAME = 'pinger'
    IP = '192.168.1.30'
    MAC = '00:1D:9C:C7:B0:03'

    def __init__(self):
        print("Hello world")
        f = open("/home/ubuntu/minicps/examples/honeypot/demofile2.txt", "w")
        f.write("Now the file has more content!")
        f.close()
        subprocess.Popen(['ip', 'addr'])
        sleep(3600)

if __name__ == "__main__":
    plc1 = Pinger()
