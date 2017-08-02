class Base(object):

    @classmethod
    def device(cls, class_name, device=None):
        pass

    @classmethod
    def topology(cls):
        pass

    @classmethod
    def run(cls):
        pass

    @classmethod
    def state(cls):
        pass

class Template(Base):

    @classmethod
    def device(cls, class_name, device="PLC"):
        return"""#{device} Template
from minicps.devices import {device}

class {class_name}({device}):

    def pre_loop(self, sleep=0.0):
        pass

    def main_loop(self, sleep=0.5):
        pass""".format(class_name=class_name, device=device)

    @classmethod
    def topology(cls):
        return"""#Topology Template

NETMASK =

from mininet.topo import Topo

class ExampleTopo(Topo):

    def build(self):
        pass"""

    @classmethod
    def run(cls):
        return """# Run Script Template
from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from topo import ExampleTopo

class ExampleCPS(MiniCPS):

    '''Main container used to run the simulation.'''

    def __init__(self, name, net):
        pass"""

    @classmethod
    def state(cls):
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
        INSERT INTO example_table VALUES ('test',   'int', '0', 1);
    '''
    return STATE, SCHEMA, SCHEMA_INIT

def init_db(path, schema, schema_init):
    SQLiteState._create(path, schema)
    SQLiteState._init(path, schema_init)"""
