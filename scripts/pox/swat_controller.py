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
import pox.lib.packet as pkt
from pox.lib.recoco import Timer
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.revent import Event, EventMixin, EventHalt

from pprint import pformat
import time

log = core.getLogger()


# TODO S:
       # check periodically the consistency of the static mapping quering the switches.
       # add nicira self-learning capability to auto-proove consistency of the mapping
       # blacklist arp spoofer
       # add switch-based init mac_to_port mapping? AntiArpPoison store a mac_to_port map
       # and send flow modification on connection up and remove flows on connection down
       # add timers to control DoS
       # get rid of ArpPoison event?
       # use class methods where necessary


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

        ip_to_mac and mac_to_port are used for dynamic (reactive) mapping.
        """

        self.connection = connection  # convenient reference
        self.connection._eventMixin_events.add(ArpPoison)

        self.ip_to_mac = {}
        self.mac_to_port = {}

        # connection_log = pformat(event.connection._eventMixin_events, indent=4)
        # log.debug("connection obj can raise those events: %s" % connection_log)

        core.openflow.addListenerByName("ConnectionUp", self._static_mapping, priority=2, once=True)
        core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp, priority=0, once=True)

        self.connection.addListenerByName("PacketIn", self._detect_arp_poison, priority=1, once=False)
        self.connection.addListenerByName("PacketIn", self._handle_PacketIn, priority=0, once=False)

        self.connection.addListenerByName("ArpPoison", self._handle_ArpPoison, priority=1, once=False)

        self.connection.addListenerByName("AggregateFlowStatsReceived", self._handle_AggregateFlowStatsReceived,
                priority=1, once=False)


# HELPER METHODS
    def drop(self, event, duration):
        """
        Drop a packet after duration 
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


    def flood(self, event):
        """
        Flood a packet 
        """
        flood_port = self.flood_port
        packet = event.parsed

        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=flood_port)
        msg.actions.append(action)

        msg.data = event.ofp  # PacketOut payload in the same as PacketIn
        msg.in_port = event.port
        # log.debug(str(msg.in_port))

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


    def get_src_addresses(self, packet):
        """
        :returns: ipsrc and macsrc as str
        """
        arp = packet.find('arp')
        if arp is not None:
            ipsrc=str(arp.protosrc)
            macsrc=str(arp.hwsrc)

        else:
            ip = packet.find('ipv4')
            if ip is not None:
                ipsrc=str(ip.srcip)
                macsrc=str(packet.src)

        # log.debug("ipsrc: %s" % (ipsrc))
        # log.debug("macsrc: %s" % (macsrc))

        return ipsrc, macsrc


    def get_dst_addresses(self, packet):
        """
        :returns: ipsrc and macsrc as str

        TODO: manage 00:00:00:00:00:00 MAC
        """
        arp = packet.find('arp')
        if arp is not None:
            ipdst=str(arp.protodst)
            macdst=str(arp.hwdst)

        else:
            ip = packet.find('ipv4')
            if ip is not None:
                ipdst=str(ip.dstip)
                macdst=str(packet.dst)

        # log.debug("ipsrc: %s" % (ipsrc))
        # log.debug("macsrc: %s" % (macsrc))

        if macdst == '00:00:00:00:00:00':
            log.debug(packet.__dict__)

        return ipdst, macdst


    def ap_detect_arp_request(self, event, packet):
        """
        Try to detect ap from an arp_request package

        Usually the attacker send some arp_request to
        its target. Notice that internal arp spoofing
        cannot be detected in this case

        :event: TODO
        :packet: TODO
        :returns: TODO

        """
        sender_ip = str(packet.payload.protosrc)
        sender_mac = str(packet.payload.hwsrc)

        dst_ip = str(packet.payload.protodst)
        dst_mac = str(packet.payload.hwdst)
    
        if sender_mac not in self.ip_to_mac.values() or sender_ip not in self.ip_to_mac:
            log.warning("on device %i: new device with %s IP and %s MAC ask info about %s IP with %s MAC" % (
                event.dpid, sender_ip, sender_mac, dst_ip, dst_mac))


    def ap_detect_arp_reply(self, event, packet):
        """
        Try to detect ap from an arp_reply package

        Usually the attacker send periodically misleading arp
        reply to target hosts.

        :event: use to retrieve information about the datapath
        :packet: arp reply payload
        :returns: flag

        """
        sender_ip = str(packet.payload.protosrc)
        sender_mac = str(packet.payload.hwsrc)

        if sender_ip in self.ip_to_mac:

            # Internal attack

            if sender_mac != self.ip_to_mac[sender_ip]:

                # Internal attack
                if sender_mac in self.ip_to_mac.values():
                    for key, value in self.ip_to_mac.items():
                        if value == sender_mac:
                            attacker_ip = key
                            break
                    log.warning("internal ap detected on device %i: %s MAC with %s IP tries to impersonate %s IP with %s MAC" % (
                        event.dpid, sender_mac, attacker_ip, sender_ip, self.static_ip_to_mac[sender_ip]))
                    return True

                # External attack
                else:
                    log.warning("external ap detected on device %i: %s MAC tries to impersonate %s IP with %s MAC" % (
                        event.dpid, sender_mac, sender_ip, self.static_ip_to_mac[sender_ip]))

                    return True

        return False


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


# HANDLERS

    def _static_mapping(self, event):
        """
        special handler for PacketIn
        add static mapping attributes to AntiArpPoison class
        init switch flooding and IPS ports
        TODO: send flow_mod related to static mapping (proactive) 
        """
        log.info("_static_mapping: %d" % self.connection.dpid)

        # TODO: use static_mac_to_port to premap switches
        self.static_ip_to_mac = swat_ip_map_1()
        self.ip_to_mac = swat_ip_map_1()

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


    def _handle_ConnectionUp(self, event):
        """
        send flowmods to statically init the switch with
        permanent flows.

        mapping is naive port 1 is used to send pkt to plc1
        ecc ...
        """
        log.info("_handle_ConnectionUp: %d" % self.connection.dpid)


    def _detect_arp_poison(self, event):
        """
        if event contains arp poisoning raise
        and ArpPoison event and block lower priority
        event handling chain.

        packet obj contains a type int attribute and
        a series of CONST_TYPE attacched to identify it

        eg: PacketIn won't trigger _handle_PacketIn
        """	

        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        arp_poisoning = False
        if packet.type == packet.ARP_TYPE:
            if packet.payload.opcode == pkt.arp.REQUEST:
                arp_poisoning = self.ap_detect_arp_request(event, packet)
            elif packet.payload.opcode == pkt.arp.REPLY:
                arp_poisoning = self.ap_detect_arp_reply(event, packet)
        # TODO: manage IPv4 packet

        if arp_poisoning:
            self.connection.raiseEvent(ArpPoison)
            log.warning("%i: Halting handling chain." % event.dpid)
            return EventHalt
        else:
            pass


    def _handle_ArpPoison(self, event):
        """
        Use it to update other switches
        """
        log.warning("_handle_ArpPoison: %d" % self.connection.dpid)

        # ap_handler_1(event)
        # ap_handler_2(event)


    def _handle_PacketIn(self, event):
        """
        Std PacketIn handling

        With flow_mod everything that is unspecified will
        be wildcarded (match everything)
        Use CIDR notation to match subnets (partial IP fileds)

        flow_mod matching rules are created using information
        from the packet_in payload

        """
        # log.info("_handle_PacketIn: %d" % self.connection.dpid)

        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        # TODO: get rid of these two helper method
        ipsrc, macsrc = self.get_src_addresses(packet)
        ipdst, macdst = self.get_dst_addresses(packet)

        self.mac_to_port[macsrc] = event.port

        if ipsrc not in self.ip_to_mac and ipsrc not in self.static_ip_to_mac:
            self.ip_to_mac[ipsrc] = macsrc
            log.info("New %s->%s pair" % (ipsrc, macsrc))

        # ????
        if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
            drop(event, 0)

        # Multicast
        elif packet.dst.is_multicast:
            log.debug("%i: flood %s -> %s" % (event.dpid, packet.src, packet.dst))
            self.flood(event)

        # Unknown destination
        elif macdst not in self.mac_to_port:
            log.info("Port from %s unknown -- flooding" % (macdst))
            self.flood(event)

        # Flow_mod
        else:
            port = self.mac_to_port[macdst]

            # don't want to forward one the same port from which the switch recieve the packet
            if port == event.port:
                log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
                        % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
                drop(event, 0)
            # add flow
            else:
                log.debug("installing flow for %s.%i -> %s.%i"
                    % (packet.src, event.port, packet.dst, port))
                msg = of.ofp_flow_mod()

                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.idle_timeout = 10  # sec
                msg.hardTimeout = 30 # sec
                action = of.ofp_action_output(port=port)
                msg.actions.append(action)
                msg.data = event.ofp  # use the same payload
                self.connection.send(msg)


    def _handle_FlowRemoved(self, event):
        """
        TODO
        """
        log.info("_handle_FlowRemoved: %d" % self.connection.dpid)


    def _handle_AggregateFlowStatsReceived(self, event):
        """
        Print event.stats list content.
        """
        log.info("_handle_AggregateFlowStatsReceived: %d" % self.connection.dpid)
        
        for stat in event.stats:
            log.info("stat: %s" % stat)


    def _handle_ConnectionDown(self, event):
        """
        TODO: remove all flow from the switch
        """
        log.info("_handle_ConnectionDown: %d" % self.connection.dpid)


def swat_ip_map_1():
    """
    six plcs and hmi.
    
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

    return ip_to_mac


def swat_port_map_1():
    """
    six plcs and hmi

    pox uses underscore MAC representation
    """

    mac_to_port = {
        '00:1d:9c:c7:b0:70': 1,
        '00:1d:9c:c8:bc:46': 2,
        '00:1d:9c:c8:bd:f2': 3,
        '00:1d:9c:c7:fa:2c': 4,
        '00:1d:9c:c8:bc:2f': 5,
        '00:1d:9c:c7:fa:2d': 6,
        '00:1d:9c:c6:72:e8': 7,
    }

    return mac_to_port


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
