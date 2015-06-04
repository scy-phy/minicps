"""
http://www.irongeek.com/i.php?page=security/security-and-software-defined-networking-sdn-openflow

it works
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.recoco import Timer
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr

from pprint import pformat

log = core.getLogger()

#The variable below are timer setting. 
#With this number, items are set to timeout on idle, and timer set to run, ever 10 sec.
TimerQuantumDuration = 10  # sec
IDS_PORT = 100

class AntiARPPoisonSwitch (object):
    """
    A AntiARPPoisonSwitch object is created for each switch that connects.
    """

    def __init__ (self, connection):
        """
        connection allows the controller to manage the switch

        AntiARPPoisonSwitch _handle methods subscribes to all connection
        event 
        eg: switch may fire a PacketIn event

        __init__ start a timer that every TimerQuantumDuration sec call
        self.timeout_callback.
        """

        self.connection = connection

        connection.addListeners(self)

        self.mac_to_port = {}
        self.ip_to_mac = {}

        # ???????
        self.ip_to_mac_time_track = {}

        #     time_to_wake,         callback           infinite loop
        Timer(TimerQuantumDuration, self.timeout_callback, recurring=True)


    # helper method used by handlers
    def send_packet (self, buffer_id, raw_data, out_port, in_port):
        """
        Sends a packet out of the specified switch port.
        If buffer_id is a valid buffer on the switch, use that. Otherwise,
        send the raw data in raw_data.
        The "in_port" is the port number that packet arrived on.    Use
        OFPP_NONE if you're generating this packet.
        """
        msg = of.ofp_packet_out()
        msg.in_port = in_port
        if buffer_id != -1 and buffer_id is not None:
            # We got a buffer ID from the switch; use that
            msg.buffer_id = buffer_id
        else:
            # No buffer ID from switch -- we got the raw data
            if raw_data is None:
                # No raw_data specified -- nothing to send!
                return
            msg.data = raw_data

        # Add an action to send to the specified port
        action = of.ofp_action_output(port = out_port)
        msg.actions.append(action)

        # Send message to switch
        self.connection.send(msg)


    #I need an index for my dictonary I can also use as an OpenFlow cookie, so I make the IP an integer             
    def int_of_ip (self, packet, packet_in):
        """
        :packet: PacketIn event.parsed
        :packet_in: PacketIn event.ofp

        :returns: source ip as an int
        """
        arp = packet.find('arp')
        if arp is not None:
            ipsrc=arp.protosrc.toUnsignedN()
        ip = packet.find('ipv4')
        if ip is not None:
            ipsrc=ip.srcip.toUnsignedN()
        return ipsrc

                    
    #Checks to see if a IP to MAC mapping is already there.
    def arp_spoof_detected(self, packet, packet_in):
        """
        :packet: PacketIn event.parsed
        :packet_in: PacketIn event.ofp

        :returns: boolean flag
        """

        # save source ip as int
        ipsrc = self.int_of_ip(packet, packet_in)

        # save MAC source as int
        arp = packet.find('arp')
        if arp is not None:
            macsrc=str(arp.hwsrc)
        ip = packet.find('ipv4')
        if ip is not None:
            macsrc=str(packet.src)

        # check duplicate entry
        if ipsrc in self.ip_to_mac:
            if self.ip_to_mac[ipsrc] != macsrc:
                return True
            #If it seems to be a new IP/MAC mapping, add it to are table, but make it timeout
            #for network flexibility. Also, new packets restart the clock for IP/MAC time outs.

        # no ARP spoofing, add a new table entry
        self.ip_to_mac[ipsrc] = macsrc

        return False

        
    #General function for checking if something looks like ARP poisoning
    def check_arp_spoof(self, packet, packet_in):
        """
        print a message in case of arp spoofing

        :packet: PacketIn event.parsed
        :packet_in: PacketIn event.ofp
        """

        if self.arp_spoof_detected(packet, packet_in):
            #Here we can put code that runs if ARP Poisoning is detected. In this case I am just alerting.
            arp = packet.find('arp')
            if arp is not None:
                tempipstring=str(self.ip_to_mac[arp.protosrc.toUnsignedN()])
                warning_message =  "Dup IP to MAC!!! " + str(arp.protosrc) + " is already taken by " + \
                    tempipstring + ". " +  str(arp.hwsrc) + " may be spoofing!"
                log.warning(warning_message)


    def act_like_switch (self, packet, packet_in):
        """
        :packet: PacketIn event.parsed
        :packet_in: PacketIn event.ofp
        """

        # save source MAC to inport mapping
        self.mac_to_port[str(packet.src)] = packet_in.in_port

        self.check_arp_spoof(packet, packet_in)

        if self.arp_spoof_detected(packet, packet_in):  
            # Maybe the log statement should have source/destination/port?
            log.debug("Installing drop flow...")

            msg = of.ofp_flow_mod()

            # Set fields to match received packet source
            msg.match=of.ofp_match(dl_src=packet.src)  # if source MAC is equal to the source

            #We don't want the flow to last forever, so we set it to time out
            #Make the blocked, potential ARP poisoner wait twice as long as other flows to time out
            msg.idle_timeout = TimerQuantumDuration * 2   # set flow_mod idle timeout

            #Output to IDS_PORT
            msg.actions.append(of.ofp_action_output(port=IDS_PORT))
            self.connection.send(msg)

        elif (str(packet.dst) in self.mac_to_port):
            log.debug('MAC '+str(packet.src)+' on port '+str(packet_in.in_port))

            # Send packet out the associated port
            self.send_packet(packet_in.buffer_id, packet_in.data, self.mac_to_port[str(packet.dst)], packet_in.in_port)
            log.debug("Installing flow...")
            # Maybe the log statement should have source/destination/port?
            msg = of.ofp_flow_mod(cookie=self.int_of_ip(packet, packet_in),flags=of.OFPFF_SEND_FLOW_REM)
            # Set fields to match received packet source
            msg.match.dl_dst=packet.dst
            #Uncomment line below to lock on more fields
            #msg.match = of.ofp_match.from_packet(packet)
            #We don't want the flow to last forever, so we set it to time out
            msg.idle_timeout = TimerQuantumDuration
            msg.actions.append(of.ofp_action_output(port = self.mac_to_port[str(packet.dst)]))
            self.connection.send(msg)

        else:
            # Flood the packet out everything but the input port
            # This part looks familiar, right?
            self.send_packet(packet_in.buffer_id, packet_in.data,
                                             of.OFPP_FLOOD, packet_in.in_port)


    # handlers
    def _handle_PacketIn (self, event):
        """
        Handles packet in messages from the switch.
        """
        packet = event.parsed # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        # packet_in contains the reference to the message obj that 
        # caused PacketIn event
        packet_in = event.ofp
        self.act_like_switch(packet, packet_in)

    
    #If the flow times out, we assume the IP to MAC address mapping is not longer in use
    def _handle_FlowRemoved (self, event):
        log.debug("Flow removed on switch %s", dpidToStr(event.dpid))
        #If I get message back that a flowhas timed out/been remove, I also remove it from the IP/MAC table
        if event.ofp.cookie in self.ip_to_mac:
            del self.ip_to_mac[event.ofp.cookie]


    #Just used for debugging, lets us show out IP/MAC table
    def timeout_callback(self):
        """
        debug function
        """

        debug_str = pformat(self.ip_to_mac, indent=4)
        log.info(debug_str)


def launch ():
    """
    Starts the component
    """
    def start_switch (event):
        """event is always a PacketIn"""
        log.debug("Controlling %s" % (event.connection,))
        AntiARPPoisonSwitch(event.connection)

    # everytime a new switch is connected start_switch is triggered
    core.openflow.addListenerByName("ConnectionUp", start_switch)
