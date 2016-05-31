"""
toy_tests.py
"""

from utils import toy_logger


def test_toy_logger():

    toy_logger.debug("TEST: debug message")
    toy_logger.info("TEST: info message")
    toy_logger.warning("TEST: warning message")
    toy_logger.error("TEST: error message")
    toy_logger.critical("TEST: critical message")
