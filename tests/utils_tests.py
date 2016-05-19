"""
utils_tests.py
"""

from minicps.utils import build_debug_logger, mcps_logger

print


def test_global_logger():

    mcps_logger.debug("TEST: debug message")
    mcps_logger.info("TEST: info message")
    mcps_logger.warning("TEST: warning message")
    mcps_logger.error("TEST: error message")
    mcps_logger.critical("TEST: critical message")


def test_build_debug_logger():

    logger = build_debug_logger('test', 10, 10)

    logger.debug("TEST: debug message")
    logger.info("TEST: info message")
    logger.warning("TEST: warning message")
    logger.error("TEST: error message")
    logger.critical("TEST: critical message")
