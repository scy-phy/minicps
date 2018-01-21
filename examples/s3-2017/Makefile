# NOTE: run iptables once then install iptables-persistent
# NOTE: run init once to generate the dbs
# NOTE: change the EC2_IP to the public EC2 IP
# NOTE: don't push passwords

EC2_ADMIN = admin
EC2_ATTACKER = attacker
EC2_IP = 54.169.211.154
EC2_WEBAPP_PORT = 8080

run:
	sudo python run.py

start:
	curl -u "$(EC2_ADMIN):$(EC2_PASSWORD)" http://$(EC2_IP):$(EC2_WEBAPP_PORT)/start

stop:
	curl -u "$(EC2_ADMIN):$(EC2_PASSWORD)" http://$(EC2_IP):$(EC2_WEBAPP_PORT)/stop

restart:
	curl -u "$(EC2_ADMIN):$(EC2_PASSWORD)" http://$(EC2_IP):$(EC2_WEBAPP_PORT)/restart

cli-pingall:
	curl -X POST -F "cmd=pingall" -F "secret=$(EC2_PASSWORD)" \
	-u "$(EC2_ADMIN):$(EC2_PASSWORD)" \
	http://$(EC2_IP):$(EC2_WEBAPP_PORT)/cli

cli-links:
	curl -X POST -F "cmd=links" -F "secret=$(EC2_PASSWORD)" \
	-u "$(EC2_ADMIN):$(EC2_PASSWORD)" \
	http://$(EC2_IP):$(EC2_WEBAPP_PORT)/cli

# NOTE: attacker has different credentials
astart:
	curl -u "$(EC2_ATTACKER):$(EC2_APASSWORD)" http://$(EC2_IP):$(EC2_WEBAPP_PORT)/start

astop:
	curl -u "$(EC2_ATTACKER):$(EC2_APASSWORD)" http://$(EC2_IP):$(EC2_WEBAPP_PORT)/stop

arestart:
	curl -u "$(EC2_ATTACKER):$(EC2_APASSWORD)" http://$(EC2_IP):$(EC2_WEBAPP_PORT)/restart
local:
	sudo python run-local.py

init:
	sudo python init.py

iptables:
	sudo sh openvpn-iptables

topo:
	sudo python topo.py

clean:
	sudo sh clean.sh

