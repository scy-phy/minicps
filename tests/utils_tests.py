"""
utils_tests.py
"""

from minicps.utils import build_debug_logger, mcps_logger

print


def test_global_logger():

    mcps_logger.debug("debug message")
    mcps_logger.info("info message")
    mcps_logger.warning("warning message")
    mcps_logger.error("error message")
    mcps_logger.critical("critical message")


def test_build_debug_logger():

    logger = build_debug_logger('test', 10, 10)

    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
