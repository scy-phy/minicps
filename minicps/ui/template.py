class BaseTemplate(object):

    @staticmethod
    def devices(number):
        pass

    @staticmethod
    def topology():
        pass

    @staticmethod
    def run():
        pass

    @staticmethod
    def state():
        pass

class Device(object):

    @staticmethod
    def plc(suffix):
        return """# PLC Template
from minicps.devices import PLC

PLC_DATA = {{
    'SENSOR1': '0',
    'SENSOR2': '0.0',
    'SENSOR3': '0',  # interlock with PLC2
    'ACTUATOR1': '1',  # 0 means OFF and 1 means ON
    'ACTUATOR2': '0',
}}

PLC_TAGS = (
    ('SENSOR1', {suffix}, 'INT'),
    ('SENSOR2', {suffix}, 'REAL'),
    ('SENSOR3', {suffix}, 'INT'),  # interlock with PLC2
    ('ACTUATOR1', {suffix}, 'INT'),  # 0 means OFF and 1 means ON
    ('ACTUATOR2', {suffix}, 'INT'))

PLC_ADDR = '10.0.0.{suffix}'

PLC_SERVER = {{
    'address': PLC_ADDR,
    'tags': PLC_TAGS
}}

PLC_PROTOCOL = {{
    'name': 'enip',
    'mode': 1,
    'server': PLC_SERVER
}}

class PLC{suffix}(PLC):

    def pre_loop(self, sleep=0.0):
        pass

    def main_loop(self, sleep=0.0):
        pass""".format(suffix=suffix)

class TemplateFactory(object):

    @staticmethod
    def getTemplate(_type):
        if _type == "default":
            return DefaultTemplate
        else:
            pass

class DefaultTemplate(BaseTemplate):

    @staticmethod
    def devices(number=1):
        return [Device.plc(suffix) for suffix in range(1, number+1)]

    @staticmethod
    def topology():
        return"""#Topology Template

from mininet.topo import Topo

NETMASK = '/24'

PLC1_MAC = '00:00:00:00:00:01'
PLC2_MAC = '00:00:00:00:00:02'

class ExampleTopo(Topo):

    def build(self):
        pass"""

    @staticmethod
    def run():
        return """# Run Script Template
from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from topo import ExampleTopo

class ExampleCPS(MiniCPS):

    '''Main container used to run the simulation.'''

    def __init__(self, name, net):
        pass"""

    @staticmethod
    def state():
        return """# state
from minicps.states import SQLiteState

def example_state():
    PATH = 'example_db.sqlite'
    NAME = 'example_table'

    STATE = {
        'name': NAME,
        'path': PATH
    }

    SCHEMA = '''
    CREATE TABLE example_table (
        name              TEXT NOT NULL,
        datatype          TEXT NOT NULL,
        value             TEXT,
        pid               INTEGER NOT NULL,
        PRIMARY KEY (name, pid)
    );
    '''

    SCHEMA_INIT = '''
        INSERT INTO example_table VALUES ('SENSOR1',   'int', '0', 1);
        INSERT INTO example_table VALUES ('SENSOR2',   'float', '0.0', 1);
        INSERT INTO example_table VALUES ('SENSOR3',   'int', '1', 1);
        INSERT INTO example_table VALUES ('ACTUATOR1', 'int', '1', 1);
        INSERT INTO example_table VALUES ('ACTUATOR2', 'int', '0', 1);
        INSERT INTO example_table VALUES ('SENSOR3',   'int', '2', 2);
    '''
    return STATE, SCHEMA, SCHEMA_INIT

def init_db(path, schema, schema_init):
    SQLiteState._create(path, schema)
    SQLiteState._init(path, schema_init)

if __name__=="__main__":
    state, schema, init = example_state()
    init_db(state['path'], schema, init)
"""
