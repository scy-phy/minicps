"""
SWaT plc1 subprocess 1 simulation
"""
import time

from constants import logger
from constants import P1_PLC1_TAGS, LIT_101, LIT_301, FIT_201
from constants import read_single_statedb, update_statedb
from constants import write_cpppo, read_cpppo, init_cpppo_server
from constants import L1_PLCS_IP
from constants import T_PLC_R, T_PLC_W
from constants import LIT_101, LIT_301, FIT_201, PLC1_CPPPO_CACHE
from constants import TIMEOUT

if __name__ == '__main__':
    """
    Init cpppo enip server.

    Execute an infinite routine loop:
        - read sensors value
        - drive actuators according to the control strategy
        - update its enip server
    """

    # init the ENIP server
    tags = []
    tags.extend(P1_PLC1_TAGS)
    init_cpppo_server(tags)
    # init ENIP server tag values
    write_cpppo(L1_PLCS_IP['plc1'], 'HMI_MV101-Status', '1')
    write_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', '2')

    # wait for the other plcs
    time.sleep(3)

    logger.debug("Enter PLC1 main loop")

    start_time = time.time()

    while(time.time() - start_time < TIMEOUT):

        # Read and update HMI_tag
        lit101_str = read_single_statedb(1, 'AI_LIT_101_LEVEL')[3]

        write_cpppo(L1_PLCS_IP['plc1'], 'HMI_LIT101-Pv', lit101_str)
        val = read_cpppo(L1_PLCS_IP['plc1'], 'HMI_LIT101-Pv', PLC1_CPPPO_CACHE)
        logger.debug("PLC1 - read_cpppo HMI_LIT101-Pv: %s" % val)

        lit101 = float(lit101_str)

        # lit101
        if lit101 >= LIT_101['HH']:
            logger.warning("PLC1 - lit101 over HH: %.2f >= %.2f" % (
                lit101, LIT_101['HH']))

        elif lit101 <= LIT_101['LL']:
            logger.warning("PLC1 - lit101 under LL: %.2f <= %.2f" % (
                lit101, LIT_101['LL']))
            # p101 = '1'  # CLOSE
            update_statedb('1', 1, 'DO_P_101_START')
            write_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', '1')
            val = read_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', PLC1_CPPPO_CACHE)
            logger.info("PLC1 - p101 closed HMI_P101-Status: %s" % val)

        elif lit101 <= LIT_101['L']:
            # mv101 = '2'  # OPEN
            update_statedb('0', 1, 'DO_MV_101_CLOSE')
            update_statedb('1', 1, 'DO_MV_101_OPEN')
            write_cpppo(L1_PLCS_IP['plc1'], 'HMI_MV101-Status', '2')
            val = read_cpppo(L1_PLCS_IP['plc1'], 'HMI_MV101-Status', PLC1_CPPPO_CACHE)
            logger.info("PLC1 - p101 open  HMI_MV101-Status: %s" % val)

        elif lit101 >= LIT_101['H']:
            # mv101 = '1'  # CLOSE
            update_statedb('1', 1, 'DO_MV_101_CLOSE')
            update_statedb('0', 1, 'DO_MV_101_OPEN')
            write_cpppo(L1_PLCS_IP['plc1'], 'HMI_MV101-Status', '1')
            val = read_cpppo(L1_PLCS_IP['plc1'], 'HMI_MV101-Status', PLC1_CPPPO_CACHE)
            logger.info("PLC1 - mv101 close HMI_MV101-Status: %s" % val)

        # read from PLC2
        val = read_cpppo(L1_PLCS_IP['plc2'], 'HMI_FIT201-Pv', PLC1_CPPPO_CACHE)
        logger.debug("PLC1 - read_cpppo HMI_FIT201-Pv: %s" % val)
        fit201 = float(val)

        # read from PLC3
        val = read_cpppo(L1_PLCS_IP['plc3'], 'HMI_LIT301-Pv', PLC1_CPPPO_CACHE)
        logger.debug("PLC1 - read_cpppo HMI_LIT301-Pv: %s" % val)
        lit301 = float(val)

        if fit201 <= FIT_201 or lit301 >= LIT_301['H']:
            # p101 = '1'  # CLOSE
            update_statedb('1', 1, 'DO_P_101_START')
            write_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', '1')
            val = read_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', PLC1_CPPPO_CACHE)
            logger.info("PLC1 - p101 closed HMI_P101-Status: %s" % val)

        elif lit301 <= LIT_301['L']:
            # p101 = '2'  # OPEN
            update_statedb('2', 1, 'DO_P_101_START')
            write_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', '2')
            val = read_cpppo(L1_PLCS_IP['plc1'], 'HMI_P101-Status', PLC1_CPPPO_CACHE)
            logger.info("PLC1 - p101 open  HMI_MV101-Status: %s" % val)

        # Sleep
        time.sleep(T_PLC_R)

    logger.debug("Exit PLC1 Main loop")
