"""
Model different type of SWaT links using TCLink subclassing.
"""

from mininet.link import TCLink


class FiberOpt(TCLink):

    """Docstring for FiberOpt. """

    def __init__(self):
        """TODO: to be defined1. """
        TCLink.__init__(self)


class EthShort(TCLink):

    """Docstring for EthShort. """

    def __init__(self):
        """TODO: to be defined1. """
        TCLink.__init__(self)

        pass


class EthLong(TCLink):

    """Docstring for EthLong. """

    def __init__(self):
        """TODO: to be defined1. """
        TCLink.__init__(self)

        pass


# Wireless
class RadioChannel(TCLink):

    """Docstring for RadioChannel. """

    def __init__(self):
        """TODO: to be defined1. """
        TCLink.__init__(self)

        pass
