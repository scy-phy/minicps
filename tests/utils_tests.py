"""
utils_tests.py
"""

from minicps.utils import build_debug_logger


def test_build_debug_logger():

    logger = build_debug_logger('test', 10, 10)

    print
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
