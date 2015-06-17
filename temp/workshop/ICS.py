from time import sleep
from time import time
from threading import Thread
import abc
import subprocess
import os
import signal

class ICS(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, tags, ipaddr, directory, timer, timeout):
        self._tags = tags
        self._ipaddr = ipaddr
        self._dir = directory
        self._timer = timer
        self.__timeout = timeout
        self.__thread = None
        self.__enip_pro = None
        self.__http_pro = None
        os.system("cd %s" % (self._dir))

    def __del__(self):
        if(self.__thread != None):
            self.__thread.join()
        if(self.__http_pro != None):
            os.killpg(self.__http_pro.pid, signal.SIGTERM)
        if(self.__enip_pro != None):
            os.killpg(self.__enip_pro.pid, signal.SIGTERM)
    
    def start_enip_server(self, file_name):
        tags = ""
        for tag_name in self._tags:
            tag_type = self._tags[tag_name]
            tags += "%s=%s " % (
                tag_name,
                tag_type)
        cmd = "python -m cpppo.server.enip -a %s -v -l %s %s &" % (
            self._ipaddr,
            self._dir + file_name,
            tags)
        self.__enip_pro = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

    def start_http_server(self, port):
        cmd = "python -m SimpleHTTPServer %d" % port
        self.__http_pro = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

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
