"""
Devices tests

time.sleep is used after net.start() to synch python interpreter with
the mininet init process.

POX prefixed ClassNames indicate controller coded into script/pox dir
and symlinked to ~/pox/pox/forwarding dir.
"""


from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI


import time
import logging
logger = logging.getLogger('minicps.devices')
setLogLevel(c.TEST_LOG_LEVEL)

