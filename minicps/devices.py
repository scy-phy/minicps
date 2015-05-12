"""
Model different type of SWaT devices using OpenFlow API
and avaliable controllers.
"""

from mininet.node import Host, Node


class POXLearningSwitch(object):

    """Docstring for POXLearningSwitch. """

    def __init__(self):
        """TODO: to be defined1. """
        pass


class PLC(Host):

    """Docstring for PLC. """

    def __init__(self):
        """TODO: to be defined1. """
        Host.__init__(self)

        pass


class DumbSwitch(Node):

    """Docstring for DumbSwitch. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class DumbRouter(Node):

    """Docstring for DumbRouter. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class Firewall(Node):

    """Docstring for Firewall. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class SCADA(Node):

    """Docstring for SCADA. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class HMI(Node):

    """Docstring for HMI. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class Historian(Node):

    """Docstring for Historian. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


# Wireless devices
class AccessPoint(Node):

    """Docstring for AccessPoint. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass
