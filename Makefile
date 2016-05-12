# regex testMatch: (?:^|[b_.-])[Tt]est)
# --exe: include also executable files
# -s: don't capture std output
TESTER = nosetests
TESTER_OPTS = -w tests -s

test:
	sudo $(TESTER) $(TESTER_OPTS)

test-minicps:
	sudo $(TESTER) $(TESTER_OPTS) minicps_tests.py

test-networks:
	sudo $(TESTER) $(TESTER_OPTS) networks_tests.py

test-sdn:
	sudo $(TESTER) $(TESTER_OPTS) sdn_tests.py

test-protocols:
	sudo $(TESTER) $(TESTER_OPTS) protocols_tests.py

test-utils:
	sudo $(TESTER) $(TESTER_OPTS) utils_tests.py
