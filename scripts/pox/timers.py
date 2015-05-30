"""
Learn:
    how to use embedded timer in core obj (for simple tasks)
    how to use lib.recoco.Timer class (tricky tasks)
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer

import time

log = core.getLogger()


def timeout_handler(*args):
    """used as a callback for the various timers

    :args: any number of values (eg: list)
    :returns: TODO

    """
    log.debug("args: %s" % (str(args)))


def timeout_handler_kill(*args):
    """

    :returns: False cancel the timer unless timer 
    constructuor set selfStoppable=False

    """
    log.debug("args: %s" % (str(args)))

    return False


def launch():
    """
    core is able to register all the pox components
    core.openflow is the pox openflow component
    _handle_ConnectionUp subscribe to core.openflow's ConnectionUp event

    each Timer instance add a non-default parameter to show Timer
    capabilities.

    """

    TIME_TO_WAKE = 2
    args = ["ciao", "mare"]
    core.callDelayed(TIME_TO_WAKE, timeout_handler, args)

    t = Timer(
            TIME_TO_WAKE,
            timeout_handler,
            args='t1')

    t2 = Timer(
            TIME_TO_WAKE,
            timeout_handler,
            absoluteTime=True,  # use False
            args='t2')

    tr = Timer(
            TIME_TO_WAKE,
            timeout_handler,
            absoluteTime=False,
            recurring=True,  # recur infinitely overtime
            args='tr')

    tw = Timer(
            TIME_TO_WAKE,
            timeout_handler,
            absoluteTime=False,
            recurring=False,
            started=False,  # not start automatically
            args='tw')
    time.sleep(TIME_TO_WAKE)
    tw.start()

    tk = Timer(
            TIME_TO_WAKE,
            timeout_handler_kill,  # handler able to cancel the timer
            absoluteTime=False,
            recurring=True,
            started=False,
            selfStoppable=False,  # timer can be cancelled by the handler
            args='tw')
