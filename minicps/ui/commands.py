"""
This file contains the commands that can be used (with parameters) both by cli
and gui packages. For example the mcps click cli is using them as subcommands.

This is the list of supported commands:

    - init
"""
import os

from template import Template

class Init(object):

    """Docstring for Init. """

    def __init__(self, cwd):
        self._cwd = cwd
        self._template = Template

    def default(self):
        path = '{}/scaffold'.format(self._cwd)
        os.makedirs(path)

        for x in range(1,3):
            with open('{}/plc{}.py'.format(path, x), 'w') as f:
                name = self._template.device('PLC{}'.format(x))
                f.write(name)

        with open('{}/topo.py'.format(path), 'w') as f:
            f.write(self._template.topology())

        with open('{}/run.py'.format(path), 'w') as f:
            f.write(self._template.run())

        with open('{}/state.py'.format(path), 'w') as f:
            f.write(self._template.state())
