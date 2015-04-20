"""
Model different type of SWaT links using TCLink subclassing.
"""

from mininet.link import Link, TCLink, TCIntf, Intf


class FiberOptIntf(TCIntf):

    """Docstring for FiberOptIntf. """

    # params = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
    params = dict(bw=10, delay='5ms')

    def config( self, bw=None, delay=None, jitter=None, loss=None,
                disable_gro=True, speedup=0, use_hfsc=False, use_tbf=False,
                latency_ms=None, enable_ecn=False, enable_red=False,
                max_queue_size=None, **params ):
        "Configure the port and set its properties."

        result = Intf.config( self, **params)

        # Disable GRO
        if disable_gro:
            self.cmd( 'ethtool -K %s gro off' % self )

        # Optimization: return if nothing else to configure
        # Question: what happens if we want to reset things?
        if ( bw is None and not delay and not loss
             and max_queue_size is None ):
            return

        # Clear existing configuration
        tcoutput = self.tc( '%s qdisc show dev %s' )
        if "priomap" not in tcoutput:
            cmds = [ '%s qdisc del dev %s root' ]
        else:
            cmds = []

        # Bandwidth limits via various methods
        bwcmds, parent = self.bwCmds( bw=bw, speedup=speedup,
                                      use_hfsc=use_hfsc, use_tbf=use_tbf,
                                      latency_ms=latency_ms,
                                      enable_ecn=enable_ecn,
                                      enable_red=enable_red )
        cmds += bwcmds

        # Delay/jitter/loss/max_queue_size using netem
        delaycmds, parent = self.delayCmds( delay=delay, jitter=jitter,
                                            loss=loss,
                                            max_queue_size=max_queue_size,
                                            parent=parent )
        cmds += delaycmds

        # Ugly but functional: display configuration info
        stuff = ( ( [ '%.2fMbit' % bw ] if bw is not None else [] ) +
                  ( [ '%s delay' % delay ] if delay is not None else [] ) +
                  ( [ '%s jitter' % jitter ] if jitter is not None else [] ) +
                  ( ['%d%% loss' % loss ] if loss is not None else [] ) +
                  ( [ 'ECN' ] if enable_ecn else [ 'RED' ]
                    if enable_red else [] ) )
        info( '(' + ' '.join( stuff ) + ') ' )

        # Execute all the commands in our node
        debug("at map stage w/cmds: %s\n" % cmds)
        tcoutputs = [ self.tc(cmd) for cmd in cmds ]
        for output in tcoutputs:
            if output != '':
                error( "*** Error: %s" % output )
        debug( "cmds:", cmds, '\n' )
        debug( "outputs:", tcoutputs, '\n' )
        result[ 'tcoutputs'] = tcoutputs
        result[ 'parent' ] = parent

        return result


class FiberOpt(TCLink):

    """Fiber optics cable connect redundant PLC for each process.
       Model: Allen-Bradley 1756-RMC1
       Datasheet: None
    """

    def __init__( self, node1, node2, port1=None, port2=None,
                  intfName1=None, intfName2=None,
                  addr1=None, addr2=None):
        Link.__init__( self, node1, node2, port1=port1, port2=port2,
                       intfName1=intfName1, intfName2=intfName2,
                       cls1=FiberOptIntf,
                       cls2=FiberOptIntf,
                       addr1=addr1, addr2=addr2,
                       )

class EthShort(TCLink):

    """Docstring for EthShort. """

    def __init__(self):
        """TODO: to be defined1. """
        TCLink.__init__(self)

        pass


class EthLong(TCLink):

    """Docstring for EthLong. """

    def __init__(self):
        """TODO: to be defined1. """
        TCLink.__init__(self)

        pass


# Wireless
class RadioChannel(TCLink):

    """Docstring for RadioChannel. """

    def __init__(self):
        """TODO: to be defined1. """
        TCLink.__init__(self)

        pass
