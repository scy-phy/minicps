"""
MAC learning switch

No dedicated Controller class.
_handle_PacketIn shows how to parse a packet using pox

Notice that this is the simplest example of a reactive(dynamic) configuration.

Prereq:
        hub.py

Learn:  
        what are core.openflow (nexus) and openflow.of_01 componenets
        what are a pox Event, Connection, ofp and Nexus objs
        what is OpenFlow's dpid and how pox manages it

        how to pass commandline arguments to pox
        how to parse a packet from an event obj
        how to construct a of_packet_out to tell the switch to flood
        how to construct a of_flow_add to tell the switch a new flow rule

        OpenFlow has a set of well defined port to flood packets

        openflow.core relevant attributes and methods
        event relevant attributes an methods
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

# global because represent the state of the whole controller
# even if it is used only _handle_PacketIn
table = {}


def decode_ofp_header(header):
    """
    :header: int code
    :returns: string 
    """

    # mirrors minicps constants
    OF10_MSG_TYPES= {
        0:  'OFPT_HELLO',  # Symmetric 
        1:  'OFPT_ERROR',  # Symmetric 
        2:  'OFPT_ECHO_REQUEST',  # Symmetric 
        3:  'OFPT_ECHO_REPLY',  # Symmetric 
        4:  'OFPT_VENDOR',  # Symmetric 

        5:  'OFPT_FEATURES_REQUEST',  # Controller -> Switch
        6:  'OFPT_FEATURES_REPLY',  # Controller -> Switch
        7:  'OFPT_GET_CONFIG_REQUEST',  # Controller -> Switch
        8:  'OFPT_GET_CONFIG_REPLY',  # Controller -> Switch
        9:  'OFPT_SET_CONFIG',  # Controller -> Switch

        10: 'OFPT_PACKET_IN',  # Async
        11: 'OFPT_FLOW_REMOVED',  # Async
        12: 'OFPT_PORT_STATUS',  # Async

        13: 'OFPT_PACKET_OUT',  # Controller -> Switch
        14: 'OFPT_FLOW_MOD',  # Controller -> Switch
        15: 'OFPT_PORT_MOD',  # Controller -> Switch

        16: 'OFPT_STATS_REQUEST',  # Controller -> Switch
        17: 'OFPT_STATS_REPLY',  # Controller -> Switch

        18: 'OFPT_BARRIER_REQUEST',  # Controller -> Switch
        19: 'OFPT_BARRIER_REPLY',  # Controller -> Switch

        20: 'OFPT_QUEUE_GET_CONFIG_REQUEST',  # Controller -> Switch
        21: 'OFPT_QUEUE_GET_CONFIG_REPLY',  # Controller -> Switch
    }

    if header in OF10_MSG_TYPES:
        return OF10_MSG_TYPES[header]
    else:
        return "%d not present" % header


def event_info(event):
    """
    event_info(event) can be used on each event handler to debug

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
    stored as a str.
    event,parsed.parsed is a bool indicating if event.parsed was correctly
    parsed

    event.ofp contains a reference to the OpenFlow message obj that caused the
    event, that can be decoded using an integer header.

    event.connection contains a reference to the path that raised that event
    """

    # OpenFlow message information
    if 'ofp' in event.__dict__:
        # log.debug("event.ofp: %s" % event.ofp)
        int_header = event.ofp.header_type
        log.info("-> event_info header type: %s" % decode_ofp_header(int_header))

    dpid = event.connection.dpid  # unique ID number for each OpenFlow Switch

    # OpenFlow payload (if present)
    if 'data' in event.__dict__:
        pkt_info = event.parsed
        if pkt_info.parsed:
            inport = event.port
            of_payload_log = pformat(pkt_info.__dict__, indent=4)
            # log.debug("event.parsed: %s" % of_payload_log)
            log.info("pkt_info: %s" % pkt_info)
            pkt_payload = pkt_info.payload
            log.info("pkt_payload: %s" % pkt_payload)
        else:
            log.info("payload sent by %s is not parseable." % dpid_to_str(dpid))

    # event and event.connection
    event_log = pformat(event.__dict__, indent=4)
    # log.debug("event: %s" % event_log)
    event_connection_log = pformat(event.connection.__dict__, indent=4)
    # log.debug("event_connection: %s" % event_connection_log)

    # dpid conversions
    connection_dpid = dpid_to_str(event.connection.dpid)
    # log.debug("connection_dpid: %s" % connection_dpid)
    connection_dpid_long = dpid_to_str(event.connection.dpid, True)  # force long format
    # log.debug("connection_dpid_long: %s" % connection_dpid_long)
    connection_eth_addr = event.connection.eth_addr
    # log.debug("connection_eth_addr: %s" % connection_eth_addr)

    log.info("<-")


def enumerate_datapaths(nexus):
    """
    nexus.connections is a variation of a python dict.
    keys are dpid (int) and values are connection references
    but the standard iterator iterates over values

    .dpids attribute returns a list dpid

    :nexus: pox obj that manages Connection objs
    :returns: integer number of connections (aka datapaths)

    """
    dpids = nexus.connections.dpids

    # std iterator over values
    # datapaths = 0
    # for connection in nexus.connections:
    #     dpid = dpids[datapaths]
    #     datapaths += 1
    #     log.debug("%i: %r with dpid %d" % (datapaths, connection, dpid))

    return len(dpids)


def blacklisted_switch(dpid):
    """
    TODO: Docstring for _blacklisted.

    :dpid: checked dpid
    :returns: bool flag

    """
    BLACKLISTED_DPID = [ 99, 100 ]

    if dpid in BLACKLISTED_DPID:
        return True
    else:
        return False


# OpenFlow handlers
def _handle_ConnectionUp(event):
    """
    Use it to manage each new datapath connection.

    ConnectionUp is raised ONLY from the nexus obj and
    it has no data field

    """
    event_info(event)

    # datapaths = enumerate_datapaths(core.openflow)
    # log.info("core.openflow manages %i connection[s]" % (datapaths))

    # dpid = event.connection.dpid
    # if blacklisted_switch(dpid):
    #     log.warning("%s with pid=%i BLACKLISTED switch connected" % (dpid_to_str(dpid), dpid))


def _handle_PacketIn(event):
    """
    PacketIn message is sent by the switch when
    its flow table contains no rule to route an
    incoming packet.

    core.openflow.miss_send_len controls the max number of
    Bytes to be sent to the Controller in each PacketIn payload
    default payload size is 128 B

    """
    event_info(event)

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

    # tell the switch two new rules -> send two flow_mod pkts
    else:

        # first rule map PacketIn source mac to
        flow_mod = of.ofp_flow_mod()

        # create matching rule
        flow_mod.match.dl_src = packet.dst
        flow_mod.match.dl_dst = packet.src

        # tell which port to use with those matching rules
        action = of.ofp_action_output(port=event.port)
        flow_mod.actions.append(action)

        event.connection.send(flow_mod)

        # do the same inverting source and destinantion 
        flow_mod = of.ofp_flow_mod()

        flow_mod.match.dl_src = packet.src
        flow_mod.match.dl_dst = packet.dst

        action = of.ofp_action_output(port=dst_port)
        flow_mod.actions.append(action)

        event.connection.send(flow_mod)

        log.info("Sent to switch rules for %s <-> %s" % (packet.src, packet.dst))


def _handle_PortStatus(event):
    """
    Controller recieve info from a datapath about
    port changes.


    """
    event_info(event)


def _handle_ConnectionDown(event):
    """
    Use it to manage each datapath disconnection.

    no event.ofp message obj
    raised both by the datapath and nexus objs

    """
    event_info(event)

    # datapaths = enumerate_datapaths(core.openflow)
    # log.info("core.openflow manages %i connection[s]" % (datapaths))

    # dpid = event.connection.dpid
    # if blacklisted_switch(dpid):
    #     log.warning("%s with pid=%i BLACKLISTED switch disconnected" % (dpid_to_str(dpid), dpid))


def launch(std_flood_port=True):
    """
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
    launch parameter are parsed as optional one

    ./pox.py log.level --DEBUG l2_pairs --std_flood_port=False

    :std_flood_port: flag to switch the port used to flood
    used because of hw switch compatibility

    """

    log.info("running.")

    if std_flood_port:
        all_ports = of.OFPP_ALL
        # log.debug("OFPP_ALL port number=%s" % (all_ports))
    else:
        all_ports = of.OFPP_FLOOD
        # log.debug("OFPP_FLOOD port number=%s" % (all_ports))

    core.openflow.addListenerByName("PacketIn", _handle_PacketIn, priority=1)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp, priority=1)
    core.openflow.addListenerByName("ConnectionDown", _handle_ConnectionDown, priority=1)
    core.openflow.addListenerByName("PortStatus", _handle_PortStatus, priority=1)
