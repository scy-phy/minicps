"""
This file contains the commands that can be used (with parameters) both by cli
and gui packages. For example the mcps click cli is using them as subcommands.

This is the list of supported commands:

    - init
"""
import os
from template import TemplateFactory

class Init(object):

    """Docstring for Init. """

    def __init__(self, cwd):
        self._cwd = cwd
        self._template = None

    def make(self, _type="default", path=None):
        if _type == "default":
            self._template = TemplateFactory.getTemplate(_type)
            self._default()
        else:
            raise NotImplementedError()

    def _default(self):
        path = '{}/scaffold'.format(self._cwd)
        os.makedirs(path)

        devices = self._template.devices(number=2)
        for idx in range(len(devices)):
            with open('{}/plc{}.py'.format(path, (idx+1)), 'w') as f:
                f.write(devices[idx])

        with open('{}/topo.py'.format(path), 'w') as f:
            f.write(self._template.topology())

        with open('{}/run.py'.format(path), 'w') as f:
            f.write(self._template.run())

        with open('{}/state.py'.format(path), 'w') as f:
            f.write(self._template.state())
