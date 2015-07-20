"""
plc1.py

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
from constants import P1_PLC1_TAGS, LIT_101, LIT_301, FIT_201
from constants import read_single_statedb, update_statedb
from constants import write_cpppo, read_cpppo, init_cpppo_server
from constants import L1_PLCS_IP
from constants import T_PLC_R, T_PLC_W
from constants import LIT_101, LIT_301, FIT_201, PLC1_CPPPO_CACHE


if __name__ == '__main__':
    """
    Init cpppo enip server.

    Execute an infinite routine loop
        - bla
        - bla
    """

    # init the ENIP server
    tags = []
    tags.extend(P1_PLC1_TAGS)
    # tags.extend(P2_PLC1_TAGS)

    # time.sleep(0.5)
    init_cpppo_server(tags)
    
    # write_cpppo(L1_PLCS_IP['plc1'], 'DO_MV_101_CLOSE', '1')
    # val = read_cpppo(L1_PLCS_IP['plc1'], 'DO_MV_101_CLOSE', 'examples/swat/plc1_cpppo.cache')
    # logger.debug("read_cpppo: %s" % val)

    # look a Stridhar graph
    c = 0
    SIM = 3
    TIN1 = ['200.0', '400.0', '600.0', '1300.0']
    TIN3 = ['200.0', '400.0', '1100.0','1300.0']
    logger.debug("Enter PLC1 main loop")
    while True:

        # Read and update HMI_tag
        update_statedb(TIN1[c], 1, 'AI_FIT_101_FLOW')
        lit101_str = read_single_statedb(1, 'AI_FIT_101_FLOW')[3]
        write_cpppo(L1_PLCS_IP['plc1'], 'HMI_LIT301-Pv', lit101_str)
        lit101 = float(lit101_str)
        logger.debug("PLC1 - lit101: %.2f" % lit101)
        # lit101 = TIN1[c]


        # Convert str into real/int
        # mv101 = int('1')
        # p101 = int('1')

        # lit101

        if lit101 >= LIT_101['HH']:
            logger.warning("PLC1 - lit101 over HH: %.2f >= %.2f" % (
                lit101, LIT_101['HH']))

        elif lit101 <= LIT_101['LL']:
            logger.warning("PLC1 - lit101 under LL: %.2f <= %.2f" % (
                lit101, LIT_101['LL']))
            p101 = '1'  # CLOSE
            logger.warning("PLC1 - stopping p101 : 2 -> %s" % (p101))

        elif lit101 <= LIT_101['L']:
            mv101 = '2'  # OPEN

        elif lit101 >= LIT_101['H']:
            mv101 = '1'  # CLOSE

        # lit301
        # lit301 = TIN3[c]
        # fit201 = float('0.6')

        # if fit201 <= FIT_201:
        #     p101 = '1'  # CLOSE

        # elif lit301 >= LIT_301['H']:
        #     p101 = '1'  # CLOSE

        # elif lit301 <= LIT_301['L']:
        #     p101 = '2'  # OPEN


        # Write back values

        # Sleep

        # DEBUG exit point
        if c >= SIM:
            break
        else:
            c += 1
