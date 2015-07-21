
"""
plc2.py

plc init:
    cpppo enip server

plc main loop:
    sequential read/write from/to the state db and its internal cpppo enip
    server.

"""
import sqlite3
import os
import time

from constants import logger
from constants import P1_PLC2_TAGS
from constants import read_single_statedb, update_statedb
from constants import write_cpppo, read_cpppo, init_cpppo_server
from constants import L1_PLCS_IP
from constants import T_PLC_R, T_PLC_W
from constants import TIMEOUT
from constants import PLC2_CPPPO_CACHE


if __name__ == '__main__':
    """
    Init cpppo enip server.

    Execute an infinite routine loop
        - bla
        - bla
    """

    # init the ENIP server
    tags = []
    tags.extend(P1_PLC2_TAGS)
    # tags.extend(P2_PLC2_TAGS)
    time.sleep(1)
    init_cpppo_server(tags)
    time.sleep(2)
    
    # write_cpppo(L1_PLCS_IP['plc2'], 'DO_MV_201_CLOSE', '2')

    # val = read_cpppo(L1_PLCS_IP['plc2'], 'DO_MV_201_CLOSE', 'examples/swat/plc2_cpppo.cache')
    # logger.debug("read_cpppo: %s" % val)

    # synch with plc2, plc3
    # time.sleep(1)

    # look a Stridhar graph
    logger.debug("Enter PLC2 main loop")
    start_time = time.time()
    while(time.time() - start_time < TIMEOUT):
        # cmd = read_single_statedb('AI_FIT_101_FLOW', '1')

        fit201pv = read_single_statedb(2, 'AI_FIT_201_FLOW')[3]

        write_cpppo(L1_PLCS_IP['plc2'], 'HMI_FIT201-Pv', fit201pv)
        val = read_cpppo(L1_PLCS_IP['plc2'], 'HMI_FIT201-Pv', PLC2_CPPPO_CACHE)
        logger.debug("PLC2 - read_cpppo HMI_FIT201-Pv: %s" % val)

        time.sleep(T_PLC_R)
    logger.debug("Exit PLC2 Main loop")

