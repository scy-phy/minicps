"""
swat_controller

based on http://www.irongeek.com/i.php?page=security/security-and-software-defined-networking-sdn-openflow

ARP poisoning resistant: passive, active, internal node, external node

the controller statically maps all switches with the ideal configuration (proactive) saving time in the init
process,

the component is event-driven and detection and mitigation code runs with higher priority than normal code.
it will be easy to develop new detection and mitigation modules and swap them into the component.

normal task mgmt is based on l2_learning provided component.

eg: if attacker detected then tell the switch to send all packet from that switch to a dedicated IDS port
eg2: if attacker detected then exclude the node from the network
eg3: reverse MITM attack using the attacker as a target and a hidden node as is target
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.recoco import Timer
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.revent import Event, EventMixin, EventHalt

from pprint import pformat

log = core.getLogger()


# TODO:
#       check periodically the consistency of the static mapping quering the switches.
#       add nicira self-learning capability to auto-proove consistency of the mapping
#       blacklist arp spoofer
#       add switch-based init mac_to_port mapping? AntiArpPoison store a mac_to_port map
#       and send flow modification on connection up and remove flows on connection down


class ArpPoison(Event):

    """ArpPoison event"""

    def __init__(self):
        Event.__init__(self)


class AntiArpPoison(object):

    """
    Class able to detect datapath ArpPoisoning

    one-time/switch ConnectionUp event is handled by _init_static function
    outside this class.
    """

    def __init__(self, event, ip_to_mac, ips_port, flood_port ):
        """
        blocking handlers: self._detect_arp_poison blocks PacketIn handling
        """

        self.connection = event.connection  # convenient reference
        self.connection._eventMixin_events.add(ArpPoison)
        self.ip_to_mac = ip_to_mac
        self.ips_port = ips_port
        self.flood_port = flood_port

        # debug attributes
        # aap_log = pformat(self.__dict__, indent=4)
        # log.debug("self.__dict__: %s" % aap_log)
        # connection_log = pformat(event.connection._eventMixin_events, indent=4)
        # log.debug("event.connection: %s" % connection_log)

        self.connection.addListenerByName("ConnectionUp", self._handle_ConnectionUp, priority=1, once=False)
        self.connection.addListenerByName("PacketIn", self._detect_arp_poison, priority=1, once=False)
        self.connection.addListenerByName("PacketIn", self._handle_PacketIn, priority=0, once=False)
        self.connection.addListenerByName("ArpPoison", self._handle_ArpPoison, priority=1, once=False)


    def drop(self, event):
        """
        Drop a packet
        """
        pass


    def flood(self, event):
        """
        Flood a packet 
        """
        flood_port = self.flood_port
        packet = event.parsed
        log.debug("flood: dataptath %i: %s -> %s" % (event.dpid, packet.src, packet.dst))

        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=flood_port)
        msg.actions.append(action)

        msg.data = event.ofp  # PacketOut payload in the same as PacketIn
        log.debug(str(msg.in_port))
        msg.in_port = event.port
        log.debug(str(msg.in_port))

        self.connection.send(msg)


    def arp_detector_1(self, event):
        """
        Try to detect arp poisoning

        :returns: flag
        """
        arp_poisoning = False

        return arp_poisoning


    def arp_detector_2(self, event):
        """
        Try to detect arp poisoning

        :returns: flag
        """
        arp_poisoning = False

        return arp_poisoning


    def _detect_arp_poison(self, event):
        """
        if event contains arp poisoning raise
        and ArpPoison event and block lower priority
        event handling chain.

        eg: PacketIn won't trigger _handle_PacketIn
        """	

        arp_poisoning = self.arp_detector_1(event)
        # arp_poisoning = self.arp_detector_2(event)

        if arp_poisoning:
            self.connection.raiseEvent(ArpPoison)
            return EventHalt
        else:
            pass


    def ap_handler_1(self, event):
        """
        redirect attacker traffic to IPS
        update all other switches
        """
        pass


    def ap_handler_2(self, event):
        """
        kick-out the attacker
        update all other switches
        """
        pass


    def _handle_ArpPoison(self, event):
        """
        Use it to update other switches
        """
        log.info("_handle_ArpPoison: %d" % event.dpid)

        # ap_handler_1(event)
        # ap_handler_2(event)


    def _handle_ConnectionUp(self, event):
        """
        TODO: send flowmods to statically init the switch
        """
        log.info("_handle_ConnectionUp: %d" % event.dpid)


    def _handle_ConnectionDown(self, event):
        """
        TODO: remove all flow from the switch
        """
        log.info("_handle_ConnectionDown: %d" % event.dpid)


    def _handle_PacketIn(self, event):
        """
        Std PacketIn handling
        """
        log.info("_handle_PacketIn: %d" % event.dpid)

        self.flood(event)
        # if multicast: # dl_dst = ff:ff:ff:ff:ff:ff
        #     flood()
        # elif already_mapped:
        #     add_flow(source, destination)
        #     add_flow(destination, source)
        # else:
        #     save_new_mapping
        #     flood()


    def _handle_FlowRemoved(self, event):
        """
        TODO
        """
        pass


def swat_map1():
    """
    six plcs and hmi.
    """

    ip_to_mac = {
            '192.168.1.10':  '00:1D:9C:C7:B0:70',
            '192.168.1.20':  '00:1D:9C:C8:BC:46',
            '192.168.1.30':  '00:1D:9C:C8:BD:F2',
            '192.168.1.40':  '00:1D:9C:C7:FA:2C',
            '192.168.1.50':  '00:1D:9C:C8:BC:2F',
            '192.168.1.60':  '00:1D:9C:C7:FA:2D',
            '192.168.1.100': '00:1D:9C:C6:72:E8',
            }

    return ip_to_mac


def _init_static(event):
    """
    Create a static mapping (proactive) 

    init switch flooding and IPS ports

    init AntiArpPoison datapath interface

    """
    log.info("_init_static: %d" % event.dpid)

    ip_to_mac = swat_map1()

    flood_port = of.OFPP_FLOOD
    # flood_port = of.OFPP_ALL

    ips_port = 4000  # used to redirect suspect traffic
    # timeout = 10  # sec, still NOT used

    AntiArpPoison(event, ip_to_mac, ips_port, flood_port)


def launch(par=False):
    """
    _init_static_mapping listens to each ConnectionUp event.
    """

    core.openflow.addListenerByName("ConnectionUp", _init_static, priority=5)
