"""
MAC learning switch
No dedicated Controller class.
_handle_PacketIn shows how to parse a packet using pox

Notice that this is the simplest example of a reactive(dynamic) configuration.

Prereq:
        study events.py

Learn:  
        what are core.openflow and openflow.of_01 componenets
        what are a pox Event, Connection and Nexus objs
        what is OpenFlow's dpid and how pox manages it

        how to pass commandline arguments to pox
        how to parse a packet from an event obj
        how to construct a of_packet_out to tell the switch to flood
        how to construct a of_flow_add to tell the switch a new flow rule

        openflow.of_01 implicit initialization
"""

# TODO: 
#       how to manually parse raw_data payloads


from pox.core import core
import pox.openflow.libopenflow_01 as of  # OpenFlow 1.0
import pox.lib.packet as pkt
from pox.lib.util import dpid_to_str

import time
from pprint import pformat  # build debug strings

log = core.getLogger()

table = {}  # table[(a, b)]


def _handle_PacketIn(event):
    """
    PacketIn message is sent by the switch when
    its flow table contains no rule to route an
    incoming packet.

    Typically there is one Connection object for
    each OpenFlow datapaths
    eg: L3EthStar topo has 1 datapath (s3)

    An OpenFlow Nexus obj manages the Connection
    objs.

    Nexus obj raises event related to all the
    datapaths in the network, a Conneciton obj
    raise events related only to a single datapath.

    Datapath mgmt can be programmed using event
    handling. Each event (in this case PacketIn)
    triggers an handler that recieve an Event obj
    as argument. The Event obj contains a reference
    to the relevant Connection obj. Indeed the handler
    can use Event obj to retrieve information about
    the request and it can use the Connection obj 
    to send messages to the datapath.
    """

    all_ports = of.OFPP_FLOOD  # 65531
    # log.debug("OFPP_FLOOD: %r" % all_ports)

    # parsed contains the openflow payload that usually is
    # the first part of the packet sent from host to s3
    packet = event.parsed


    # table is indexed by a tuple (connection, mac_address)
    src_key = (event.connection, packet.src)
    table[src_key] = event.port
    # log.debug("controller add new table entry: %r: %r" % (
        # src_key, table[src_key]))

    # built key given the MAC destination 
    # and search the table for destination port
    dst_key = (event.connection, packet.dst)
    dst_port = table.get(dst_key)

    # tell the switch to flood -> send a of_packet_out pkt
    if dst_port is None:
        # data is a reference to the event that called that function
        of_packet_out = of.ofp_packet_out(data=event.ofp)

        # create a flood action
        action = of.ofp_action_output(port=all_ports)
        of_packet_out.actions.append(action)

        # send the of_packet_out
        event.connection.send(of_packet_out)

    # tell the switch two new rules -> send two of_flow_add pkts
    else:

        # first rule map PacketIn source mac to
        of_flow_add = of.ofp_flow_mod()

        # create matching rule
        of_flow_add.match.dl_src = packet.dst
        of_flow_add.match.dl_dst = packet.src

        # tell which port to use with those matching rules
        action = of.ofp_action_output(port=event.port)
        of_flow_add.actions.append(action)

        event.connection.send(of_flow_add)

        # do the same inverting source and destinantion 
        of_flow_add = of.ofp_flow_mod()

        of_flow_add.match.dl_src = packet.src
        of_flow_add.match.dl_dst = packet.dst

        action = of.ofp_action_output(port=dst_port)
        of_flow_add.actions.append(action)

        event.connection.send(of_flow_add)

        log.debug("Sent to switch rules for %s <-> %s" % (packet.src, packet.dst))


def _dissect_PacketIn(event):
    """
    dpid is unique identifier value that a switch send to the
    controller during their handshake ofp_switch_feature
    can be retrived from event.connection.dpid (int)
    and event.connection.eth_src (string)

    dpid format is xx-xx-xx-xx-xx-xx|n
    xx-xx-xx-xx-xx-xx is stored by pox as an integer
    the |n part is optional, usually is set to 0 and it is 
    reserved to switch implementers

    pox.lib.util contains dpid conversion functions
    eg: dpid_to_str, str_to_dpid

    mininet assign dpid incrementally according to switchname
    eg: s3 will have dpid = 3
    WARNING do NOT Use --mac option -> h3 and s3 will have the same MAC

    event.parsed contains the payload of the OpenFlow protocol (no header)
    event.ofp contains a reference to the OpenFlow message that caused the
    event
    """

    packet = event.parsed

    # DEBUG strings
    event_log = pformat(event.__dict__, indent=4)
    log.debug("event: %s" % event_log)
    event_connection_log = pformat(event.connection.__dict__, indent=4)
    log.debug("event_connection: %s" % event_connection_log)

    connection_dpid = dpid_to_str(event.connection.dpid)
    log.debug("connection_dpid: %s" % connection_dpid)
    connection_dpid_long = dpid_to_str(event.connection.dpid, True)  # force long format
    log.debug("connection_dpid_long: %s" % connection_dpid_long)
    connection_eth_addr = event.connection.eth_addr
    log.debug("connection_eth_addr: %s" % connection_eth_addr)

    inport = event.port
    dpid = event.connection.dpid  # unique ID number for each OpenFlow Switch
    if not packet.parsed:
        log.warning("%i %i ignoring unparsed packet", dpid, inport)
        return

    payload = packet.payload
    # log.debug("first packet %r, with payload: %r with dpid=%r and inport=%r"
            # % (packet, payload, dpid, inport))


def _enumerate_datapaths(nexus):
    """TODO: Docstring for _enumerate_paths.

    :nexus: pox obj that manages Connection objs
    :returns: integer number of connections

    """
    datapaths = 0

    for connection in nexus.connections:
        datapaths += 1
        log.debug("%i: %r" % (datapaths, connection))

    return datapaths


def _handle_ConnectionUp(event):
    """
    Use it to manage each new datapath connection.

    """
    datapaths = _enumerate_datapaths(core.openflow)
    log.info("core.openflow manages %i connection[s]" % (datapaths))


def _handle_ConnectionDown(event):
    """
    Use it to manage each datapath disconnection.

    """
    datapaths = _enumerate_datapaths(core.openflow)
    log.info("core.openflow manages %i connection[s]" % (datapaths))


# TODO: understand disable_flood, difference bt OFPP_FLOOD and OFPP_ALL
def launch(disable_flood=False):
    """TODO: Docstring for launch.

    :disable_flood: TODO
    :returns: TODO

    """
    log.info("running.")

    all_ports = of.OFPP_FLOOD
    # log.debug("OFPP_FLOOD port number=%s" % (all_ports))

    if disable_flood:
        all_ports = of.OFPP_ALL
        log.debug("OFPP_ALL port number=%s" % (all_ports))

    core.openflow.addListenerByName("PacketIn", _handle_PacketIn, priority=1)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp, priority=1)
    core.openflow.addListenerByName("ConnectionDown", _handle_ConnectionDown, priority=1)

    # uncomment to obtain detalied informaiton about relevant data objs
    # event_class, event_id = core.openflow.addListenerByName("PacketIn", _dissect_PacketIn, priority=2)
