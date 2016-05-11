TESTER = nosetests
TESTER_OPTS =

test:
	sudo $(TESTER) $(TESTER_OPTS) tests/

test-minicps:
	sudo $(TESTER) $(TESTER_OPTS) tests/minicps_tests.py

test-networks:
	sudo $(TESTER) $(TESTER_OPTS) tests/networks_tests.py

test-sdn:
	sudo $(TESTER) $(TESTER_OPTS) tests/sdn_tests.py

test-protocols:
	sudo $(TESTER) $(TESTER_OPTS) tests/protocols_tests.py

test-utils:
	sudo $(TESTER) $(TESTER_OPTS) tests/utils_tests.py
