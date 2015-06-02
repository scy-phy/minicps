"""
Hub implementation. 

No dedicated Controller class.
Only one callback function that is called once during ConnectionUp
that instructs all the switches to flood every packet to every port 
except the one whose the packet was coming from.

Notice that this is the simplest example of a proactive(static) configuration.

Prereq:
        study events.py

Learn: 
    pox uses OpenFlow v1.0 protocol (eg: of_flow_mod insted of of_flow_add)
    what is the launch function
    what is an action
    how to subscribe to an event setting a callback (handler) function
    what is _handle_ConnectionUp event
    OpenFlow has a set of well defined port to flood packets
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.util import dpidToStr

import time

# wrapper around logger.getLogger()
log = core.getLogger()

def _handle_ConnectionUp(event):
    """
    handle ConnectionUp event that is raised once
    the controller is connected.

    :event: object carrying all the info to the controller

    addListenerByName permits to specify the handler function
    giving the name of the event (raised by core.openflow)
    """

    # construct of_flowmod message
    msg = of.ofp_flow_mod()  # create of_flowmod  message
    action = of.ofp_action_output(port=of.OFPP_FLOOD)  # create an output to port action
    msg.actions.append(action)  # append action to the of_flowmod

    # send it
    event.connection.send(msg)  # send msg to the switch

    dest_pid = dpidToStr(event.dpid)  # extract the destination(switch) process id
    log.debug("controller send %s to node %s." % (msg, dest_pid))
    log.info("%s act like a hub.", dest_pid)


def launch():
    """
    core is able to register all the pox components
    core.openflow is the pox openflow component
    _handle_ConnectionUp subscribe to core.openflow's ConnectionUp event

    """

    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.info("Hub running")
