#!/usr/bin/env python

"""
Script to perform pox init.

Pox dir defaults to ~/pox
minicps dir defaults to ~/minicps

Use POX_COMPONENTS list to add new symlinks.
Use -v for verbose and -vv for colored verbose.
"""

import argparse
import os

POX_COMPONENTS = [
    'antiarppoison.py',
    'hub.py',
    'l2_pairs.py',
    'l2_learning.py',
]

SWAT = [
    'pox_controller.py',
]

PARSER_DESC = 'perform minicps pox init'
parser = argparse.ArgumentParser(description=PARSER_DESC)
parser.add_argument(
    "-v", "--verbose",
    help='print more info',
    action="count",
    default=0)
parser.add_argument(
    "-p", "--pox",
    help='pox dir (defaults to ~/pox)',
    default='~/pox')
parser.add_argument(
    "-m", "--minicps",
    help='minicps dir (defaults to ~/minicps)',
    default='~/minicps')

args = parser.parse_args()
print "pox path is: %s" % args.pox
print "minicps path is: %s" % args.minicps

choice = raw_input('please confirm: [Yn]')

if choice == 'n' or choice == 'no':
    print "Abort init.py"

else:
    # POX scripts
    TARGET = '%s/scripts/pox' % args.minicps
    LINK = '%s/ext' % args.pox
    for c in POX_COMPONENTS:
        command = 'ln -s %s/%s %s/%s' % (TARGET, c, LINK, c)
        # print "DEBUG:", command
        os.system(command)

        if args.verbose >= 2:
            vv_command = 'ls --color=auto -l %s/%s' % (LINK, c)
            os.system(vv_command)

        elif args.verbose >= 1:
            v_command = 'ls -l %s/%s' % (LINK, c)
            os.system(v_command)

    # SWAT
    TARGET = '%s/examples/swat' % args.minicps
    for c in SWAT:
        command = 'ln -s %s/%s %s/%s' % (TARGET, c, LINK, c)
        # print "DEBUG:", command
        os.system(command)

        if args.verbose >= 2:
            vv_command = 'ls --color=auto -l %s/%s' % (LINK, c)
            os.system(vv_command)

        elif args.verbose >= 1:
            v_command = 'ls -l %s/%s' % (LINK, c)
            os.system(v_command)
