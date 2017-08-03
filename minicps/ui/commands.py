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
            self._default(path)
        else:
            raise NotImplementedError("Only default is supported.")

    def _default(self, path):
        dir_path = '{}/{}'.format(self._cwd, path)
        os.makedirs(dir_path)

        devices = self._template.devices(number=2)
        for idx in range(len(devices)):
            self._create('{}/plc{}.py'.format(path, (idx+1)), devices[idx])
            self._display("{path}/plc{idx}.py".format(folder=folder, idx=idx+1))

        self._create('{}/run.py'.format(path), self._template.run())
        self._create('{}/state.py'.format(path), self._template.state())
        self._create('{}/topo.py'.format(path), self._template.topology())

        self._display("{folder}/state.py".format(folder=folder))
        self._display("{folder}/run.py".format(folder=folder))
        self._display("{folder}/topo.py".format(folder=folder))

    def _create(self, path, message):
        with open(path, 'w') as f:
            f.write(message)

    def _display(self, message):
        print "{:<5} create {}".format("", message)

