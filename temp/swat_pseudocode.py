# swat_controller

"""
Code is portable because additiona featrues are implemented as higher
priority handlers. Indeed further additional features improvement can
easily substitute older features
eg: _detect_arp_poison can be replaced with _detect_arp_poison_super 

Conventional handler are in the form of _handle_EventName
and higher priority handlers are in the form _do_something_nice, 
helper functions are in the form do_something.

"""

class AntiArpPosoning(object):
    """Class able to detect datapath ArpPoisoning """

    
    def __init__(self, event, mac_to_port):
        self.event = event
        self.mac_to_port = mac_to_port
        
        # TODO: how to use priority in this case?
        event.connection = addListeners(self)


    def drop(event):
	    """
	    Drop a packet
	    """

	
    def flood(event):
	    """
	    Flood a packet 
	    """

	
    def detect_arp_poison(event):
        """
        Try to detect arp poisoning
        """


    def _detect_arp_poison(event):
        """
        listens to all events that can cause arp_poisoning
        """"	
        
	    arp_poisoning = detect_arp_poison(event)
	
	    if arp_poisoning:
	        # diffeerent solutions
	        monitor_attacker()
	        kick_out_attacker()		
    
	
    def _handle_ConnectionUp(event):
	    """
	    TODO
	    """
	
	    enable_timers()
	
	
    def _handle_ConnectionDown(event):
	    """
	    TODO
	    """
	
    def _handle_PacketIn(event):
	    """
	    TODO
	    """
	
	    if multicast:
	        flood()
        elif already_mapped:
            add_flow(source, destination)
            add_flow(destination, source)
        else:
            save_new_mapping
            flood()
           
            
    def _handle_FlowRemoved(event):
	    """
	    TODO
	    """
            
            
def _init_static_mapping(event):
	"""
	Create a static mapping (proactive) 
	and init the ArpPoisoning instance.
	
	"""
	
	mac_to_port = swat_l1()
	
	ArpPoisoning(event, mac_to_port)
	    
	        
def swat_l1():
    """
    TODO: take values from constants.py
    """


def launch():
    """
    _init_static_mapping listens to each ConnectionUp event.
    """
    
    core.openflow.addListenerbyname("ConnectionUp", _init_static_mapping, priority=5)

	    
