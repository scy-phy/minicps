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
import time

log = core.getLogger()


# TODO:
#       check periodically the consistency of the static mapping quering the switches.
#       add nicira self-learning capability to auto-proove consistency of the mapping
#       blacklist arp spoofer
#       add switch-based init mac_to_port mapping? AntiArpPoison store a mac_to_port map
#       and send flow modification on connection up and remove flows on connection down
#       add timers to control DoS


class ArpPoison(Event):

    """
    By default core.openflow and connection can raise the same
    set of events.

    ArpPoison is added only to the connection obj set.
    """

    # TODO: Remove __init__
    def __init__(self):
        Event.__init__(self)


class AntiArpPoison(object):

    """
    Class able to detect datapath ArpPoisoning

    one-time/switch ConnectionUp event is handled by _init_static function
    outside this class.
    """

    def __init__(self, connection):
        """
        blocking handlers: self._detect_arp_poison blocks PacketIn handling

        ConnectionUp handler are called only once because core.openflow will
        raise one ConnectionUp event for each switch
        """

        self.connection = connection  # convenient reference
        self.connection._eventMixin_events.add(ArpPoison)

        # connection_log = pformat(event.connection._eventMixin_events, indent=4)
        # log.debug("connection obj can raise those events: %s" % connection_log)

        # once=True because core.openflow will raise 
        core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp, priority=0, once=True)

        self.connection.addListenerByName("PacketIn", self._static_mapping, priority=2, once=True)
        self.connection.addListenerByName("PacketIn", self._detect_arp_poison, priority=1, once=False)
        self.connection.addListenerByName("PacketIn", self._handle_PacketIn, priority=0, once=False)

        self.connection.addListenerByName("ArpPoison", self._handle_ArpPoison, priority=1, once=False)

        self.connection.addListenerByName("AggregateFlowStatsReceived", self._handle_AggregateFlowStatsReceived,
                priority=1, once=False)


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


    def request_stats(self, stat=2):
        """
        TODO: don't know how to build and send msg

        Send an ofp_stats_request from the controller

        :stat_type: see of.OFPST_XXXXX int constants
        defaults to OFPST_AGGREGATE
        """
        pass
        # msg = of.ofp_stats_request()
        # log.debug("request stat: %s %d" % (type(stat), state))
        # ofp_stats_request_log = pformat(msg.__dict__, indent=4)
        # log.debug("ofp_stats_request: %s" % ofp_stats_request_log)
        # msg.type(stat_type)
        # self.connection.send(msg)


    def ap_detector_1(self, event):
        """
        Try to detect arp poisoning

        :returns: flag
        """
        arp_poisoning = False

        return arp_poisoning


    def ap_detector_2(self, event):
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

        arp_poisoning = self.ap_detector_1(event)
        # arp_poisoning = self.ap_detector_2(event)

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
        log.warning("_handle_ArpPoison: %d" % event.dpid)

        # ap_handler_1(event)
        # ap_handler_2(event)


    def _handle_ConnectionUp(self, event):
        """
        send flowmods to statically init the switch with
        permanent flows.

        mapping is naive port 1 is used to send pkt to plc1
        ecc ...
        """
        log.info("_handle_ConnectionUp: %d" % event.dpid)


    def _handle_ConnectionDown(self, event):
        """
        TODO: remove all flow from the switch
        """
        log.info("_handle_ConnectionDown: %d" % event.dpid)


    def _static_mapping(self, event):
        """
        special handler for PacketIn
        add static mapping attribute to AntiArpPoison class
        init switch flooding and IPS ports
        TODO: send flow_mod related to static mapping (proactive) 
        """
        log.info("_static_mapping: %d" % event.dpid)

        self.ip_to_mac, self.mac_to_port = swat_map1()
        self.flood_port = of.OFPP_FLOOD
        # self.flood_port = of.OFPP_ALL
        self.ips_port = 4000  # used to redirect suspect traffic
        # self.timeout = 10  # sec, still NOT used

        # debug attributes
        # aap_log = pformat(self.__dict__, indent=4)
        # log.debug("self.__dict__: %s" % aap_log)

        # self.connection.send( of.ofp_flow_mod ( action=of.ofp_action_output(port=2),
        #                                         match = of.ofp_match( dl_dst = 'ff:ff:ff:ff:ff:ff')))

        # for mac, port in self.mac_to_port.items():
        #     # log.debug("key: %s value: %s" % (mac, port))
        #     msg = of.ofp_flow_mod()
        #     msg.idle_timeout = of.OFP_FLOW_PERMANENT
        #     msg.hard_timeout = of.OFP_FLOW_PERMANENT
        #     # msg.match.dl_type = 0x800  # match only IP packets
        #     msg.match.dl_dst = mac
        #     action = of.ofp_action_output(port=port)  # then forward packet to port
        #     msg.actions.append(action)
        #     self.connection.send(msg)
        #     time.sleep(2)
                                                                          
        return EventHalt


    def _handle_PacketIn(self, event):
        """
        Std PacketIn handling
        """
        log.info("_handle_PacketIn: %d" % event.dpid)

        pass

        # self.flood(event)
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
        log.info("_handle_FlowRemoved: %d" % event.dpid)


    def _handle_AggregateFlowStatsReceived(self, event):
        """
        Print event.stats list content.
        """
        log.info("_handle_AggregateFlowStatsReceived: %d" % event.dpid)
        
        for stat in event.stats:
            log.info("stat: %s" % stat)


def swat_map1():
    """
    six plcs and hmi.
    
    pox uses underscore MAC representation
    """

    ip_to_mac = {
        '192.168.1.10':  '00:1d:9c:c7:b0:70',
        '192.168.1.20':  '00:1d:9c:c8:bc:46',
        '192.168.1.30':  '00:1d:9c:c8:bd:f2',
        '192.168.1.40':  '00:1d:9c:c7:fa:2c',
        '192.168.1.50':  '00:1d:9c:c8:bc:2f',
        '192.168.1.60':  '00:1d:9c:c7:fa:2d',
        '192.168.1.100': '00:1d:9c:c6:72:e8',
    }

    mac_to_port = {
        '00:1d:9c:c7:b0:70': 1,
        '00:1d:9c:c8:bc:46': 2,
        '00:1d:9c:c8:bd:f2': 3,
        '00:1d:9c:c7:fa:2c': 4,
        '00:1d:9c:c8:bc:2f': 5,
        '00:1d:9c:c7:fa:2d': 6,
        '00:1d:9c:c6:72:e8': 7,
    }

    return ip_to_mac, mac_to_port


def _init_datapath(event):
    """
    special handler to init one AntiArpPoison obj
    for each new datapath.
    """

    AntiArpPoison(event.connection)


def launch(par=False):
    """
    _init_static_mapping listens to each ConnectionUp event.

    core.openflow raise ConnectionUp for each new datapath.

    event represents messages from switch to the controller
    and are managed using _handlers

    connection obj manage messages from the controller to
    the switch because it allows to send of messages.
    
    """

    # nexus_log = pformat(core.openflow._eventMixin_events, indent=4)
    # log.debug("core.openflow obj can raise those events: %s" % nexus_log)

    core.openflow.addListenerByName("ConnectionUp", _init_datapath, priority=2)
