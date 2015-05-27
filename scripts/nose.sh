#!/bin/bash

# typical testing commands
sudo nosetests -s -v tests/
sudo nosetests -s tests/
sudo nosetests -s tests/devices_tests.py
sudo nosetests -s tests/devices_tests.py:fun_name

# report: term, term-missing, html, xml, annotate
# --cov set the covered FS
sudo nosetests -s --with-cov --cov-report annotate --cov . tests/devices_tests.py
