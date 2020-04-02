from time import sleep

from srve import Srve
from constants import Constants
from mininet.log import info

from Logger import hlog
import cpppo.server.enip.client as client

class Clie:
    NAME = 'clie'
    IP = '192.168.1.10'
    MAC = '00:1D:9C:C7:B0:10'

    def __init__(self):
        hlog("Hello client")
        sleep(5)
        hlog("Hello client2")
        client.main([
            '--verbose',
            '--print',
            '--address', Srve.IP + ":" + str(Constants.ENIP_TCP_PORT),
            '--log', Constants.ENIP_LOG_FILE,
            'Scada[1]=99'])

if __name__ == "__main__":
    Clie()