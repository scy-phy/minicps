import random
from time import sleep
from srvm import Srvm
from constants import Constants
from mininet.log import info

from Logger import hlog
from cpppo.server.enip import client

class Clie:
    NAME = 'clie'
    IP = '192.168.1.10'
    MAC = '00:1D:9C:C7:B0:10'

    def __init__(self):
        hlog("Hello world")
        client.main(['-a', '1.2.3.4'])

if __name__ == "__main__":
    Clie()