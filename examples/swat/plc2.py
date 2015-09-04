"""
plc2.py

plc init:
    cpppo enip server

plc main loop:
    sequential read/write from/to the state db and its internal cpppo enip
    server.

"""
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

    # init the ENIP server
    tags = []
    tags.extend(P1_PLC2_TAGS)
    time.sleep(1)
    init_cpppo_server(tags)
    time.sleep(2)

    logger.debug("Enter PLC2 main loop")
    start_time = time.time()
    while(time.time() - start_time < TIMEOUT):

        fit201pv = read_single_statedb(2, 'AI_FIT_201_FLOW')[3]

        write_cpppo(L1_PLCS_IP['plc2'], 'HMI_FIT201-Pv', fit201pv)
        val = read_cpppo(L1_PLCS_IP['plc2'], 'HMI_FIT201-Pv', PLC2_CPPPO_CACHE)
        logger.debug("PLC2 - read_cpppo HMI_FIT201-Pv: %s" % val)

        time.sleep(T_PLC_R)
    logger.debug("Exit PLC2 Main loop")
