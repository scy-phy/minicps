TESTER = nosetests
TESTER_OPTS =

test:
	sudo $(TESTER) $(TESTER_OPTS) tests/

test-minicps:
	sudo $(TESTER) $(TESTER_OPTS) tests/minicps_tests.py

test-networks:
	sudo $(TESTER) $(TESTER_OPTS) tests/minicps_networks.py

test-sdn:
	sudo $(TESTER) $(TESTER_OPTS) tests/minicps_sdn.py

test-protocols:
	sudo $(TESTER) $(TESTER_OPTS) tests/minicps_protocols.py

test-utils:
	sudo $(TESTER) $(TESTER_OPTS) tests/minicps_utils.py
