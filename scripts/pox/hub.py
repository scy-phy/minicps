"""
Hub implementation. 
No dedicated Controller class.
Only one callback function that is called once during ConnectionUp
that instructs all the switches to flood every packet to every port 
except the one whose the packet was coming from.

Notice that this is the simplest example of a proactive(static) configuration.

Learn: launch function, how to subscribe to an event setting a callback (handler) function
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.util import dpidToStr

import time

log = core.getLogger()

def _handle_ConnectionUp(event):
    """handler naming convention does't apply in this case

    :event: object carrying all the info to the controller
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

    event_class, event_id = core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.info("Hub running")
