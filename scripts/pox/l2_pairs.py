"""
MAC learning switch
No dedicated Controller class.
_handle_PacketIn shows how to parse a packet using pox

Notice that this is the simplest example of a reactive(dynamic) configuration.

Learn:  
        how pox components model work
        how to create an object able to raise events, create a new event class,
        how to setup handler priority
        how to stop an event using an handler
        how to set-up a One-time event,
        how to unsubscribe to an event
"""

# TODO: how to subscribe EventRaiser to the pox core

from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.revent import Event, EventMixin, EventHalt

import time

log = core.getLogger()

table = {}  # table[(a, b)]


class EventName(Event):

    """event that can be raised by EventRaiser"""

    def __init__(self):
        """TODO: to be defined1. """
        Event.__init__(self)
        log.debug("Inside EventName")


class EventRaiser(EventMixin):

    """obj able to raise events"""

    _eventMixin_events = set([
        EventName,
    ])
        

def _handle_EventName(event):
    """EvenName handler function

    :event: revent.Event
    """
    log.debug("callback: _handle_EventName")


def _handle_EventName_urgent(event):
    """see addListener in the launch function for the priority

    :returns: optional block the event otherwise pass the 
    control to the next handler according to priority
    """

    log.debug("callback: _handle_EventName_urgent")
    # return EventHalt
        

def _handle_EventName_onetime(event):
    """see addListener in the launch function for once

    :event: revent.Event

    """
    log.debug("callback: _handle_EventName_onetime")


def _handle_PacketIn(event):
    """PacketIn message is sent by the switch when
    its flow table contains no rule to route an
    incoming packet.
    """

    all_ports = of.OFPP_FLOOD

    packet = event.parsed  # parse the relevant packet info

    src_key = (event.connection, packet.src)
    # log.debug('src_key: %s' % str(src_key))

    table[src_key] = event.port  # controller store source

    dst_key = (event.connection, packet.dst)
    # log.debug('dst_key: %s' % str(dst_key))

    dst_port = table.get(dst_key)

    if dst_port is None:  # flood
        msg = of.ofp_packet_out(data=event.ofp)  # create a packet_out msg
        action = of.ofp_action_output(port=all_ports)
        msg.actions.append(action)
        event.connection.send(msg)

    else:  # flow_mod install rule

        # first flow_mod 
        msg = of.ofp_flow_mod()  # create a flow_mod message
        msg.match.dl_dst = packet.src
        msg.match.dl_src = packet.dst
        action = of.ofp_action_output(port=event.port)
        msg.actions.append(action)
        event.connection.send(msg)

        # second flow_mod
        msg = of.ofp_flow_mod()  # create a flow_mod message
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst
        action = of.ofp_action_output(port=dst_port)
        msg.actions.append(action)
        event.connection.send(msg)

        log.debug("Rules for %s <-> %s" % (packet.src, packet.dst))


def launch(disable_flood=False):
    """TODO: Docstring for launch.

    :disable_flood: TODO
    :returns: TODO

    """

    all_ports = of.OFPP_FLOOD
    log.debug("OFPP_FLOOD port number=%s" % (all_ports))

    if disable_flood:
        all_ports = of.OFPP_ALL
        log.debug("OFPP_ALL port number=%s" % (all_ports))

    event_class, event_id = core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("l2_pairs is running.")

    raiser = EventRaiser()
    # default priority is unknown
    event_class, event_id = raiser.addListener(EventName, _handle_EventName, priority=0)
    event_class, event_id = raiser.addListener(EventName, _handle_EventName_urgent, priority=2)
    event_class, event_id = raiser.addListener(EventName, _handle_EventName_onetime,
            once=True, priority=-1)

    for x in range(3):
        raiser.raiseEvent(EventName)
        time.sleep(1)

    rc = core.openflow.removeListener(event_id)
    log.debug("core.openflow doesn't listen to %s with EID:%s? %r" % (event_class, event_id, rc))

