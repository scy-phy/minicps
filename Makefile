# MiniCPS makefile

# VARIABLES {{{1
MININET = sudo mn

PYTHON = sudo python
PYTHON_OPTS = 

# TODO: add testing conditionals for verbosity, doctest plugin and coverage plugin
# http://web.mit.edu/gnu/doc/html/make_7.html
TESTER = sudo nosetests
TESTER_OPTS = -s -v --exe
TESTER_OPTS_COV_HTML = $(TESTER_OPTS) --with-coverage --cover-html

# TOY {{{1

toy:
	cd examples/toy; $(PYTHON) $(PYTHON_OPTS) run.py; cd ../..

test-toy:
	cd examples/toy; $(TESTER) $(TESTER_OPTS) tests.py; cd ../..

# TODO: test
test-toy-cover:
	cd examples/toy; $(TESTER) $(TESTER_OPTS_COV_HTML) tests.py; cd ../..

# SWAT {{{1

swat-s1:
	cd examples/swat-s1; $(PYTHON) $(PYTHON_OPTS) run.py; cd ../..

test-swat-s1:
	cd examples/swat-s1; $(TESTER) $(TESTER_OPTS) tests.py; cd ../..

# TODO: restructure dirs
# swat-tutorial:
# 	cd examples/swat; \
# 	$(PYTHON) $(PYTHON_OPTS) tutorial/run.py
# 	cd ../..
# test-swat:
# 	$(TESTER) $(TESTER_OPTS) examples/swat/tests


# STATE {{{1

kill-cpppo:
	sudo pkill  -f -u root "python -m cpppo.server.enip"

# MINICPS TESTS {{{1

# regex testMatch: (?:^|[b_.-])[Tt]est)
# --exe: include also executable files
# -s: don't capture std output
# nosetests -s tests/devices_tests.py:fun_name

test:
	$(TESTER) $(TESTER_OPTS) tests

# https://pypi.python.org/pypi/nose-cov/1.6
# FIXME: test cov
# report: term, term-missing, html, xml, annotate
# --cov set the covered FS
# test-cov:
# 	sudo $(TESTER) $(TESTER_OPTS_COV) minicps_tests.py

test-mcps:
	$(TESTER) $(TESTER_OPTS) tests/mcps_tests.py

test-networks:
	$(TESTER) $(TESTER_OPTS) tests/networks_tests.py

test-sdn:
	$(TESTER) $(TESTER_OPTS) tests/sdn_tests.py

test-protocols:
	$(TESTER) $(TESTER_OPTS) tests/protocols_tests.py

test-utils:
	$(TESTER) $(TESTER_OPTS) tests/utils_tests.py

test-state:
	$(TESTER) $(TESTER_OPTS) tests/state_tests.py

test-devices:
	$(TESTER) $(TESTER_OPTS) tests/devices_tests.py


# clean {{{1
clean: clean-cover, clan-pyc, clean-logs

clean-cover:
	rm -f minicps/*,cover
	rm -f tests/*,cover

clean-pyc:
	rm -f minicps/*.pyc
	rm -f tests/*.pyc

clean-logs:
	rm -f logs/*.log
