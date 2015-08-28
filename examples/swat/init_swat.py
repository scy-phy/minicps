"""
SWaT DB initialization
"""

from constants import update_statedb
from constants import logger

if __name__ == '__main__':
    logger.debug('DB - initialization...')
    update_statedb(700, 'AI_LIT_301_LEVEL')
    update_statedb(400, 'AI_LIT_101_LEVEL')
    update_statedb(2, 'DO_P_101_START')
    update_statedb(1, 'DO_MV_101_OPEN')
    update_statedb(1, 'DO_MV_201_OPEN')
    update_statedb(0.7, 'AI_FIT_101_FLOW')
    update_statedb(0.5, 'AI_FIT_201_FLOW')
    update_statedb(0, 'DO_MV_101_CLOSE')
    update_statedb(0, 'DO_MV_201_CLOSE')
    logger.debug('DB - initialized')
