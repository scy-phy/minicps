"""
SWaT physical process
"""

import sqlite3
from constants import VALVE_DIAMETER
from constants import TANK_DIAMETER
from constants import PROCESS_NUMBER
from constants import GRAVITATION
from constants import TIMER
from constants import TIMEOUT
from constants import P1_INPUT_FLOW
from constants import P1_INPUT_VALVES
from constants import P1_OUTPUT_VALVES
from constants import STATE_DB_PATH
from constants import TABLE
from time import sleep
from time import time
from math import sqrt as sqrt
from math import pow as power

###################################
#         PHYSICAL PROCESS
###################################

def flow_to_height(flow, diameter):
    """
    flow: flow value (m^3/h)
    diameter: tank diameter (m^2)

    returns: height per hour corresponding (m/h)
    """
    return flow / diameter

def speed_to_height(speed, valve_diameter, tank_diameter):
    """
    speed: speed of water in a pipe (m/s)
    valve_diameter: (m)
    tank_diamaeter: (m)

    returns: height per second corresponding in the tank (m/s)
    """
    return speed * power(valve_diameter, 2) / power(tank_diameter, 2)

def Toricelli(flow_level, valve_height):
    """
    Toricelli formula, which returns the speed of the flow (m/s) according to
    the flow level in the tank and the valve height,
    considering the speed as a constant in the Bernoulli formula.
    """
    return sqrt(2 * GRAVITATION * (flow_level - valve_height))

def compute_new_flow_level(FIT_list, MV_list, LIT, P_list, tank_diameter, valve_diameter, timer):
    """
    FIT_list: list of input flow values (int, m^3/s)
    MV_list: list of boolean which tell if the valve is open or not
    LIT: current flow level (m)
    P_list: list of output valves which tells if they are open or not
    tank_diameter: (m)
    valves: (m)
    timer: period in which the flow level is computed (s)

    returns: new flow level (m)
    """
    height = LIT
    for i in input_list:
        if MV_list[i] != 0:
            # FIT_list[i] is supposed to be in m^3/h and timer in seconds => conversion
            height += (timer/3600) * flow_to_height(FIT_list[i], diameter)
    for i in P_list:
        if P_LIST[i] != 0:
            # Toricelli formula gives the speed in m/s => no conversion
            height -= timer * speed_to_height(Toricelli(LIT, 0), valve_diameter, tank_diameter)
    return height

###################################
#          CONTROLLER
###################################
def fetch_value(db_path, table, field, pid):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cmd = 'SELECT VALUE FROM %s WHERE NAME="%s" AND PID=%d;' % (table,
                                                                   field,
                                                                   pid)
        cursor.execute(cmd)
        record = cursor.fetchone()
    return record

def update_value(db_path, table, field, pid, value):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cmd = 'UPDATE %s SET VALUE=%d WHERE NAME="%s" AND PID=%d;' % (table,
                                                                        value,
                                                                        field,
                                                                        pid)
        cursor.execute(cmd)
        conn.commit()

###################################
#               MAIN
###################################
if __name__ == '__main__':
    """
    main thread
    """
    start_time = time()
    while(time() - start_time < TIMEOUT):
        for i in range(0,PROCESS_NUMBER):
            input_flows = []
            input_valves = []
            output_valves = []

            for index in P1_INPUT_FLOW:
                input_flows.append(fetch_value(STATE_DB_PATH, TABLE, index, i))
            for index in P1_INPUT_VALVES:
                input_valves.append(fetch_value(STATE_DB_PATH, TABLE, index, i))
            for index in P1_OUTPUT_VALVES:
                output_valves.append(fetch_value(STATE_DB_PATH, TABLE, index, i))
            current_flow = fetch_value(STATE_DB_PATH, TABLE, 'AI_LIT_%d01_LEVEL' % i, i)
            new_flow = compute_new_flow_level(input_flows, input_valves, current_flow, output_valves, TANK_DIAMETER, VALVE_DIAMETER, TIMER)

            update_value(STATE_DB_PATH, TABLE, 'AI_LIT_%d01_LEVEL' % i, i, new_flow)
            sleep(TIMER)
