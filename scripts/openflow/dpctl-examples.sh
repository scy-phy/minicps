# https://github.com/mininet/mininet/wiki/FAQ#why-doesnt-dpctl-work-how-can-i-dump-a-switchs-flow-table

# many OpenFlow switches (ovsk) automatically opens 
# port number 6634 for remote debugging

# show switch capability
dpctl show tcp:127.0.0.1:6634

# Show switch flow table stats
dpctl dump-flows tcp:127.0.0.1:6634

# Manially add flow entries with default 60s timeout
dpctl add-flow tcp:127.0.0.1:6634 in_port=1,actions=output:2

# Manially add flow entries setting the timeout
dpctl add-flow tcp:127.0.0.1:6634 in_port=1,idle_timeout=120,actions=output:2

# Std OpenFlow controller port is 6633

# Std controller - switch init
# of_hello ... of_hello
# of_features_request ... of_features_reply 
# of_set config

# Keep alive messages starts from the switch
# echo_request ... echo_reply

# Std switch - controller dialog
# of_packet_in ... of_packet_out
#              ,,, of_flow_add
# of_flow_expired

# Message type codes
# see constants

# Convenient filter to ignore keep alive msgs
# of && (of.type != 3) && (of.type != 2)
