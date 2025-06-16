# This script allows traffic to be routed to/from mininet.
# It expects a local network interface to be named enp0s3
# After its execution all traffic from mininet is briged to enp0s3
# Change LOCAL_INTERFACE to name of real interface where honeypot is installed

LOCAL_INTERFACE=enp0s3

sudo ifconfig s1 up
sudo ovs-vsctl add-port s1 $LOCAL_INTERFACE
sudo ifconfig $LOCAL_INTERFACE
sudo dhclient s1
