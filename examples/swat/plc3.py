"""
plc3.py

plc init:
    cpppo enip server

plc main loop:
    sequential read/write from/to the state db and its internal cpppo enip
    server.

"""
import time

from constants import logger
from constants import P1_PLC3_TAGS
from constants import read_single_statedb, update_statedb
from constants import write_cpppo, read_cpppo, init_cpppo_server
from constants import L1_PLCS_IP
from constants import T_PLC_R, T_PLC_W
from constants import TIMEOUT
from constants import PLC3_CPPPO_CACHE

if __name__ == '__main__':

    # init the ENIP server
    tags = []
    tags.extend(P1_PLC3_TAGS)
    time.sleep(2)
    init_cpppo_server(tags)
    time.sleep(1)

    logger.debug("Enter PLC3 main loop")
    start_time = time.time()
    while(time.time() - start_time < TIMEOUT):

        lit301pv = read_single_statedb(3, 'AI_LIT_301_LEVEL')[3]

        write_cpppo(L1_PLCS_IP['plc3'], 'HMI_LIT301-Pv', lit301pv)
        val = read_cpppo(L1_PLCS_IP['plc3'], 'HMI_LIT301-Pv', PLC3_CPPPO_CACHE)
        logger.debug("PLC3 - read_cpppo HMI_LIT301-Pv: %s" % val)

        time.sleep(T_PLC_R)
    logger.debug("Exit PLC3 Main loop")
