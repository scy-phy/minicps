"""
Flow based learing switch

l2_learning listens to openflow events and uses a dedicated
class called LearningSwitch to manage the Switch learning logic
eg: flood, flow_mod, drop

Learn:
    how to create a dedicate controller class

    how to pass commandline arguments to pox
    how to register a pox component to the core object
    how to drop a packet
    how to flood multicast packets (eg: ARP request uses 00:00:00:00:00:00)
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

import pox.lib.packet as pkt

from pox.lib.util import dpid_to_str  # convert process id to string
from pox.lib.util import str_to_bool  # return True given a set of string keywords

import time

log = core.getLogger()

_flood_delay = 0


class LearningSwitch(object):

    """
    Create a LearningSwitch OpenFlow API
    for each switch in the network
    """

    def __init__(self, connection, transparent):
        """TODO: to be defined1.

        :connection: TODO
        :transparent: TODO

        """
        self.connection = connection
        self.transparent = transparent
        
        # controller MACs table
        self.macToPort = {}

        # Every _handle_EventName (subsribers) will be mapped to
        # EventName (raised event)
        connection.addListeners(self)

        # Bool to track a timer
        self.hold_down_expired = (_flood_delay == 0)

        log.debug("Initializing LearningSwitch, transparent=%s",
                str(self.transparent))


    def _handle_PacketIn(self, event):
        """
        flood mgmt

        """
        packet = event.parsed


        def flood(message=None):
            """TODO: Docstring for flood.

            """
            msg = of.ofp_packet_out()  # create of_packet_out
            if time.time() - self.connection.connect_time >= _flood_delay:
                if self.hold_down_expired is False:
                    self.hold_down_expired = True
                    log.info("%s: Flood hold_down expired -- flooding",
                            dpid_to_str(event.dpid))
                if message is not None: log.debug(message)
                log.debug("%i: flood %s -> %s" % (event.dpid, packet.src, packet.dst))
                action = of.ofp_action_output(port=of.OFPP_FLOOD)
                msg.actions.append(action)
            else:
                log.info("Holding down flood for %s" % (dpid_to_str(event.dpid)))
                pass
            msg.data = event.ofp
            msg.in_port = event.port
            self.connection.send(msg)


        def drop(duration=None):
            """TODO: Docstring for drop.

            """
            if duration is not None:
                if not isinstance(duration, tuple):  # idle_timeout, hard_timeout
                    duration = (duration, duration)
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet)
                msg.idle_timeout = duration[0]
                msg.hard_timeout = duration[1]
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                self.connection.send(msg)
            elif event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                self,connection.send(msg)


        self.macToPort[packet.src] = event.port

        if not self.transparent:
            if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
                drop()
                return

        if packet.dst.is_multicast:
            flood()
        else:
            if packet.dst not in self.macToPort:
                flood("Port from %s unknown -- flooding" % (packet.dst))
            else:
                port = self.macToPort[packet.dst]
                if port == event.port:
                    log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
                            % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
                    drop(10)
                    return
                log.debug("installing flow for %s.%i -> %s.%i"
                    % (packet.src, event.port, packet.dst, port))
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.idle_timeout = 10
                msg.hard_timeout = 30
                action = of.ofp_action_output(port=port)
                msg.actions.append(action)
                msg.data = event.ofp
                self.connection.send(msg)


class l2_learning(object):

    """
    l2_learning pox component that used L3EthStarAttack
    class to manage flood and flow_mod events.
    """

    def __init__(self, transparent):
        """TODO: to be defined1.

        :transparent: passed through command line

        """

        # l2_learning obj subscribes to core.openflow components events
        core.openflow.addListeners(self)

        self.transparent = transparent

    def _handle_ConnectionUp(self, event):
        """
        Event fired once the controller is connected

        """

        log.debug("Connection %s" % (event.connection))

        LearningSwitch(event.connection, self.transparent)


def launch(transparent=False, hold_down=_flood_delay):
    """
    launch argument are parsed from command line

    """
    try:
        global _flood_delay
        _flood_delay = int(str(hold_down), 10)  # base 10 conversion
        assert _flood_delay >= 0
    except:
        raise RuntimeError("Expected hold_down to be a number.")

    # create an instance of a l2_learning class
    # passing transparent to its constructor
    # assigning the classname as component name
    # eg: core.l2_learning
    core.registerNew(l2_learning, str_to_bool(transparent))
        
