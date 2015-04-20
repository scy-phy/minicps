"""
links module unit-tests.
"""

from nose.tools import *
import minicps

from mininet.topo import MinimalTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Host, OVSSwitch, Controller, Link

from minicps.links import FiberOpt


def setup():
    print 'SETUP'


def teardown():
    print 'TEAR DOWN!'


def test_fiber():
    """TODO: Docstring for test_fiber.

    """

    net = Mininet(topo=MinimalTopo(),
                  link=FiberOpt)
    net.start()

    net.pingAll()
    print "Testing bandwidth"
    net.iperf()

    net.stop()

    #low-level API
    # h1 = Host( 'h1' )
    # h2 = Host( 'h2' )                                                                                                     
    # s1 = OVSSwitch( 's1', inNamespace=False )                                                                             
    # c0 = Controller( 'c0', inNamespace=False )                                                                            
    # FiberOpt( h1, s1 )                                                                                                        
    # FiberOpt( h2, s1 )                                                                                                        
    # h1.setIP( '10.1/8' )                                                                                                  
    # h2.setIP( '10.2/8' )                                                                                                  
    # c0.start()                                                                                                            
    # s1.start( [ c0 ] )                                                                                                    
    # print h1.cmd( 'ping -c1', h2.IP() )                                                                                   
    # print h2.cmd( 'ping -c1', h1.IP() )                                                                                   
    # s1.stop()                                                                                                             
    # c0.stop() 
