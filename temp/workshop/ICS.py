from time import sleep
from time import time
from threading import Thread
import abc
from os import system

class ICS(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, tags, ipaddr, timer, timeout):
        self._tags = tags
        self._ipaddr = ipaddr
        self._timer = timer
        self.__timeout = timeout
        self.__thread = None

    def __del__(self):
        if(self.__thread != None):
            self.__thread.join()
    
    def start_server(self, file_name):
        tags = ""
        for tag_name in self._tags:
            tag_type = self._tags[tag_name]
            tags += "%s=%s " % (
                tag_name,
                tag_type)
        system("python -m cpppo.server.enip -a %s -v -l %s %s &" % (
            self._ipaddr,
            file_name,
            tags))

    @abc.abstractmethod
    def action(self): # input
        """Method documentation"""
        return

    def action_wrapper(self):
        start_time = time()
        while(time() - start_time < self.__timeout):
            sleep(self._timer)
            self.action()

    def run(self):
        self.__thread = Thread(target = self.action_wrapper())
        self.__thread.start()
