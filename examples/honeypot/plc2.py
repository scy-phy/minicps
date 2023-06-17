from datetime import time

from minicps.devices import PLC


class Plc2(PLC):
    NAME = 'plc2'
    IP = '192.168.1.20'
    MAC = '00:1D:9C:C7:B0:02'
    STATE = {
        'name': 'honeypot',
        'path': 'honeypot_db.sqlite'
    }
    TAGS = (
        ('FIT101', 1, 'REAL'),
        ('MV101', 1, 'INT'),
        ('LIT101', 1, 'REAL'),
        ('P101', 1, 'INT'),
        # interlocks does NOT go to the statedb
        ('FIT201', 1, 'REAL'),
        ('MV201', 1, 'INT'),
        ('LIT301', 1, 'REAL'),
    )

    SERVER = {
        'address': IP,
        'tags': TAGS
    }
    PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': SERVER
    }
    DATA = {
        'TODO': 'TODO',
    }
    def __init__(self):
        PLC.__init__(self,
            name=self.name,
            state= Plc2.STATE,
            protocol=Plc2.PROTOCOL,
            memory=Plc2.DATA,
            disk=Plc2.DATA)

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: plc2 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        print 'DEBUG: plc2 enters main_loop.'
        print

if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc1 = Plc2()
