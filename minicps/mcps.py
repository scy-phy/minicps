"""
mcps.py

Main module for functional classes.

MiniCPS augments Mininet capabilities in the context of Cyber-Physical
Systems.
"""

import sys
from mininet.cli import CLI


# TODO: maybe return some pid
class MiniCPS(object):

    """Main container used to run the simulation."""

    # TODO: validate inputs

    def __init__(self, name, net, path):
        """MiniCPS initialization steps:

        net object usually contains reference to:
            - the topology
            - the link shaping
            - the CPU allocation
            - the [remote] SDN controller

        :name: CPS name
        :net: Mininet object
        :path: string containig the cps root folder path
        """

        self.name = name
        self.net = net
        self.path = path

        self._hosts = net.hosts

        self.net.start()

        cmd = ''
        for host in self._hosts:
            if host.name == 'c0' or host.name == 's1':
                continue
            else:
                cmd = sys.executable + ' ' + \
                    self.path + '/' + host.name + '.py &'
                print 'DEBUG MiniCPS cmd: ', cmd
                host.cmd(cmd)

        CLI(self.net)

        self.net.stop()
