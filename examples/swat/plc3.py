
"""
SWaT plc3 subprocess 1 simulation
"""
import sqlite3
import os
import time

from constants import logger
from constants import P1_PLC3_TAGS
from constants import read_single_statedb, update_statedb
from constants import write_cpppo, read_cpppo, init_cpppo_server
from constants import L1_PLCS_IP
from constants import T_PLC_R, T_PLC_W, TIMEOUT
from constants import PLC3_CPPPO_CACHE


if __name__ == '__main__':
    """
    Init cpppo enip server.

    Execute an infinite routine loop:
        - read UF tank level from the sensor
        - update internal enip server
    """

    # init the ENIP server
    tags = []
    tags.extend(P1_PLC3_TAGS)
    # tags.extend(P2_PLC3_TAGS)
    time.sleep(2)
    init_cpppo_server(tags)

    # wait for the other plcs
    time.sleep(1)
    
    # write_cpppo(L1_PLCS_IP['plc3'], 'AI_LIT_301_LEVEL', '3')
    # val = read_cpppo(L1_PLCS_IP['plc3'], 'AI_LIT_301_LEVEL', 'examples/swat/plc3_cpppo.cache')
    # logger.debug("read_cpppo: %s" % val)

    logger.info("PLC3 - enters main loop")

    start_time = time.time()

    while(time.time() - start_time < TIMEOUT):
        # cmd = read_single_statedb('AI_FIT_101_FLOW', '1')

        lit301pv = read_single_statedb('3', 'AI_LIT_301_LEVEL')[3]

        write_cpppo(L1_PLCS_IP['plc3'], 'HMI_LIT301-Pv', lit301pv)
        val = read_cpppo(L1_PLCS_IP['plc3'], 'HMI_LIT301-Pv', PLC3_CPPPO_CACHE)
        logger.debug("PLC3 - read_cpppo HMI_LIT301-Pv: %s" % val)

        time.sleep(T_PLC_R)
    logger.info("PLC3 - exits main loop")

