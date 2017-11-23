import os
import shutil

from minicps.ui.commands import Init
from minicps.ui.template import TemplateFactory, DefaultTemplate, Device

from nose.tools import eq_
from nose.plugins.skip import SkipTest

class TestInit():

    def test_initialization(self):
        init = Init()
        eq_(init._template, None)

    def test_make_creates_directory_with_default_files(self):
        init = Init()
        init.make("../scaffold")

        eq_(init._template, DefaultTemplate)
        assert os.path.isdir("../scaffold".format(os.getcwd()))

        shutil.rmtree('../scaffold')

    def test_make_raises_NotImplementedError_when_type_is_not_default(self):
        init = Init()
        try:
            init.make("./scaffold", _type="[placholder]")
            assert False
        except NotImplementedError as e:
            assert True
            shutil.rmtree('./scaffold')

    def test__default_creates_default_files(self):
        os.mkdir('./default')

        init = Init()
        init._template = TemplateFactory.get_template('default')
        init._default('./default')

        assert os.path.exists("./default/plc1.py")
        assert os.path.exists("./default/plc2.py")
        assert os.path.exists("./default/run.py")
        assert os.path.exists("./default/topo.py")
        assert os.path.exists("./default/state.py")

        shutil.rmtree('./default')

    def test__create_makes_a_new_file(self):
        init = Init()
        init._create('test.py', "test")

        assert os.path.exists('./test.py')

        os.remove('./test.py')

class TestTemplateFactory():

    def test_factory_template_generator_for_default_path(self):
        eq_(TemplateFactory.get_template("default"), DefaultTemplate)

    def test_factory_template_generator_raises_error_for_other_path(self):
        try:
            TemplateFactory.get_template("[placeholder]")
            assert False
        except NotImplementedError as e:
            assert True

class TestDefaultTemplate():

    def test_default_devices_with_argument_number_greater_than_3(self):
        test = DefaultTemplate.devices(number=3)
        eq_(len(test), 3)

    def test_default_devices_with_default_argument(self):
        test = DefaultTemplate.devices()
        eq_(len(test), 1)

    def test_default_topology(self):
        res = "#Topology Template\n\nfrom mininet.topo import Topo\n\nNETMASK = '/24'\n\nPLC1_MAC = '00:00:00:00:00:01'\nPLC2_MAC = '00:00:00:00:00:02'\n\nclass ExampleTopo(Topo):\n\n    def build(self):\n        pass"
        eq_(DefaultTemplate.topology(), res)

    def test_default_run(self):
        res = "# Run Script Template\nfrom mininet.net import Mininet\nfrom mininet.cli import CLI\nfrom minicps.mcps import MiniCPS\nfrom topo import ExampleTopo\n\nclass ExampleCPS(MiniCPS):\n\n    '''Main container used to run the simulation.'''\n\n    def __init__(self, name, net):\n        pass"
        eq_(DefaultTemplate.run(), res)

    def test_default_state(self):
        res = '# state\nfrom minicps.states import SQLiteState\n\ndef example_state():\n    PATH = \'example_db.sqlite\'\n    NAME = \'example_table\'\n\n    STATE = {\n        \'name\': NAME,\n        \'path\': PATH\n    }\n\n    SCHEMA = \'\'\'\n    CREATE TABLE example_table (\n        name              TEXT NOT NULL,\n        datatype          TEXT NOT NULL,\n        value             TEXT,\n        pid               INTEGER NOT NULL,\n        PRIMARY KEY (name, pid)\n    );\n    \'\'\'\n\n    SCHEMA_INIT = \'\'\'\n        INSERT INTO example_table VALUES (\'SENSOR1\',   \'int\', \'0\', 1);\n        INSERT INTO example_table VALUES (\'SENSOR2\',   \'float\', \'0.0\', 1);\n        INSERT INTO example_table VALUES (\'SENSOR3\',   \'int\', \'1\', 1);\n        INSERT INTO example_table VALUES (\'ACTUATOR1\', \'int\', \'1\', 1);\n        INSERT INTO example_table VALUES (\'ACTUATOR2\', \'int\', \'0\', 1);\n        INSERT INTO example_table VALUES (\'SENSOR3\',   \'int\', \'2\', 2);\n    \'\'\'\n    return STATE, SCHEMA, SCHEMA_INIT\n\ndef init_db(path, schema, schema_init):\n    SQLiteState._create(path, schema)\n    SQLiteState._init(path, schema_init)\n\nif __name__=="__main__":\n    state, schema, init = example_state()\n    init_db(state[\'path\'], schema, init)\n'
        eq_(DefaultTemplate.state(), res)

class TestDevice():

    def test_plc(self):
        res = "# PLC Template\nfrom minicps.devices import PLC\n\nPLC_DATA = {\n    'SENSOR1': '0',\n    'SENSOR2': '0.0',\n    'SENSOR3': '0',  # interlock with PLC2\n    'ACTUATOR1': '1',  # 0 means OFF and 1 means ON\n    'ACTUATOR2': '0',\n}\n\nPLC_TAGS = (\n    ('SENSOR1', 1, 'INT'),\n    ('SENSOR2', 1, 'REAL'),\n    ('SENSOR3', 1, 'INT'),  # interlock with PLC2\n    ('ACTUATOR1', 1, 'INT'),  # 0 means OFF and 1 means ON\n    ('ACTUATOR2', 1, 'INT'))\n\nPLC_ADDR = '10.0.0.1'\n\nPLC_SERVER = {\n    'address': PLC_ADDR,\n    'tags': PLC_TAGS\n}\n\nPLC_PROTOCOL = {\n    'name': 'enip',\n    'mode': 1,\n    'server': PLC_SERVER\n}\n\nclass PLC1(PLC):\n\n    def pre_loop(self, sleep=0.0):\n        pass\n\n    def main_loop(self, sleep=0.0):\n        pass"
        eq_(Device.plc(1), res)
