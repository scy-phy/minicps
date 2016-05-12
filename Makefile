# regex testMatch: (?:^|[b_.-])[Tt]est)
# --exe: include also executable files
# -s: don't capture std output

# test {{{1
# TODO: add testing conditionals for verbosity, doctest plugin and coverage plugin
# http://web.mit.edu/gnu/doc/html/make_7.html
TESTER = nosetests
TESTER_OPTS = -w tests -s -v --noexe
TESTER_OPTS_COV = -w tests -s -v --noexe --with-cov --cov-report annotate


test:
	sudo $(TESTER) $(TESTER_OPTS)

# https://pypi.python.org/pypi/nose-cov/1.6
# FIXME: test cov
# test-cov:
# 	sudo $(TESTER) $(TESTER_OPTS_COV) minicps_tests.py

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


# clean {{{1
clean: clean-cover

clean-cover:
	rm -f minicps/*,cover
	rm -f tests/*,cover

clean-pyc:
	rm -f minicps/*.pyc
	rm -f tests/*.pyc
