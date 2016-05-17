"""
toy utils.py
"""

PLC1_TAG_DICT = {
    'SENSOR1' '0',
    'SENSOR2' '0.0',
    'SENSOR3' '0',  # interlock with PLC2
    'ACTUATOR1' '1',  # 0 means OFF and 1 means ON
    'ACTUATOR2' '0',
}
PLC2_TAG_DICT = {
    'SENSOR3' '0',  # interlock with PLC1
}

PLC1_MAC = '00:00:00:00:00:01'
PLC1_ADDR = '10.0.0.1'

PLC2_ADDR = '10.0.0.2'
PLC2_MAC = '00:00:00:00:00:02'

DB_PATH = 'examples/toy/db.sqlite'
