"""
toy utils.py
"""

PLC1_TAG_DICT = {
    'SENSOR1': '0',
    'SENSOR2': '0.0',
    'SENSOR3': '0',  # interlock with PLC2
    'ACTUATOR1': '1',  # 0 means OFF and 1 means ON
    'ACTUATOR2': '0',
}
PLC2_TAG_DICT = {
    'SENSOR3': '0',  # interlock with PLC1
}

PLC1_MAC = '00:00:00:00:00:01'
PLC1_ADDR = '10.0.0.1'

PLC2_ADDR = '10.0.0.2'
PLC2_MAC = '00:00:00:00:00:02'

# state info
PATH = 'examples/toy/toy_db.sqlite'
NAME = 'toy_table'
SCHEMA = """
CREATE TABLE toy_table (
    name              TEXT NOT NULL,
    datatype          TEXT NOT NULL,
    value             TEXT,
    pid               INTEGER NOT NULL,
    PRIMARY KEY (name, pid)
);
"""
SCHEMA_INIT = """
    INSERT INTO toy_table VALUES ('SENSOR1',   'int', '0', 1);
    INSERT INTO toy_table VALUES ('SENSOR2',   'float', '0.0', 1);
    INSERT INTO toy_table VALUES ('SENSOR3',   'int', '1', 1);
    INSERT INTO toy_table VALUES ('SENSOR3',   'int', '2', 2);
    INSERT INTO toy_table VALUES ('ACTUATOR1', 'int', '1', 1);
    INSERT INTO toy_table VALUES ('ACTUATOR2', 'int', '0', 1);
"""
