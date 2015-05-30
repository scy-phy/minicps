"""
pox event handling

events maps communication from the OpenFlow datapaths (eg switches) to
the controller. This mapping is saved in a set of pox components able to
raise an event according to the incoming packet. The control program has
to specify a set of handlers (functions) to respond to events.

Multiple functions with different features (eg: priority) may be mapped
to the same event. An event handler is able to stop or forward the event
to the next handler (eg: packet filter)

OpenFlow list of event classes: pox/pox/openflow/__init__.py

Learn:    
        how to create an object able to raise events, create a new event class,
        how to setup handler priority (pox default priority in unspecified)
        how to stop an event using an handler
        how to set-up a One-time event,
        how to unsubscribe to an event

"""

from pox.core import core
from pox.lib.revent import Event, EventMixin, EventHalt

import time

from pprint import pformat  # build debug strings

log = core.getLogger()


class EventName(Event):

    """event that can be raised by EventRaiser"""

    def __init__(self):
        """TODO: to be defined1. """
        Event.__init__(self)


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


def launch():
    """
    TODO

    """
    
    raiser = EventRaiser()

    raiser_listeners_ids = {}  # store info related to raiser listeners id

    # default priority is unknown, you can use negative priority
    # addListener returns a tuple
    event_class, handler_id = raiser.addListener(EventName, _handle_EventName, priority=0)
    raiser_listeners_ids['_handle_EventName'] = handler_id

    event_class, handler_id = raiser.addListener(EventName, _handle_EventName_urgent, priority=2)
    raiser_listeners_ids['_handle_EventName_urgent'] = handler_id
    log.debug("event_class: %r" % (event_class))
    log.debug("handler_id: %r" % (handler_id))

    event_class, handler_id = raiser.addListener(EventName, _handle_EventName_onetime,
            once=True, priority=-1)
    raiser_listeners_ids['_handle_EventName_onetime'] = handler_id

    for x in range(3):
        log.info("raiser raised EventName")
        raiser.raiseEvent(EventName)
        time.sleep(1)

    log.info("Removed _handle_EventName_urgent subscription to core.openflow's EventName")
    rc = raiser.removeListener(raiser_listeners_ids['_handle_EventName_urgent'])

    for x in range(3):
        raiser.raiseEvent(EventName)
        time.sleep(1)
