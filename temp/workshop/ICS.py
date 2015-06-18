from threading import Thread
from time import sleep
from time import time
import abc
import os
import signal
import subprocess

class ICS(object):
    """
    ICS class represents every kind of machine in the MiniCPS network such as plc, workstation, hmi
    it needs an IP adress, a main directory,
    timer and timeout seconds in order to execute an action() every timer seconds during timeout seconds
    a tags dictionary in case of ENIP communications, in order to start a ENIP server. It associates
    the tag names with their type, e.g. tags = { 'flow': 'REAL', 'pump': 'INT'}
    """
    #Abstract class, because the action() method has to be implemented by subclasses
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, tags, ipaddr, directory, timer, timeout):
        """
        This constructor initialize all the ICS class attributes
        """
        self._tags = tags
        self._ipaddr = ipaddr
        self._dir = directory
        self._timer = timer
        self.__timeout = timeout
        # This thread will execute the action() method every timer seconds during timeout seconds
        self.__thread = None
        # Store server processes information, in order to stop them in the destructor
        self.__enip_proc = None
        self.__http_proc = None
        os.system("cd %s" % (self._dir))

    def __del__(self):
        """
        This desctructor joins the action() thread, and stop the servers running on the ICS machine
        """
        if(self.__thread != None):
            self.__thread.join()
        if(self.__http_proc != None):
            os.killpg(self.__http_proc.pid, signal.SIGTERM)
        if(self.__enip_proc != None):
            os.killpg(self.__enip_proc.pid, signal.SIGTERM)
    
    def start_enip_server(self, file_name):
        """
        This method launch a ENIP server on the ICS machine using the tags passed in argument of the constructor
        It also records this ENIP server output in a file named file_name
        """
        # Concatenate all ENIP tags in a string
        tags = ""
        for tag_name in self._tags:
            tag_type = self._tags[tag_name]
            tags += "%s=%s " % (
                tag_name,
                tag_type)
        # Launch the ENIP server
        cmd = "python -m cpppo.server.enip -a %s -v -l %s %s &" % (
            self._ipaddr,
            self._dir + file_name,
            tags)
        # Store process informations in order to be able to stop it in the destructor
        self.__enip_proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

    def start_http_server(self, port):
        """
        Starts a simple http server on a choosen port
        """
        cmd = "python -m SimpleHTTPServer %d" % port
        self.__http_proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

    @abc.abstractmethod
    def action(self):
        """
        This is an abstract method wich has to be implemented by the subclasses
        It allows subclasses to run any action (e.g. monitoring by querying a ENIP server for a hmi, reading sensors and changing state of actuators for a plc)
        """
        return

    def action_wrapper(self):
        """
        Main loop for the action() thread
        every timer seconds during timeout seconds
        """
        start_time = time()
        while(time() - start_time < self.__timeout):
            sleep(self._timer)
            self.action()

    def run(self):
        """
        Runs the action() thread
        """
        self.__thread = Thread(target = self.action_wrapper())
        self.__thread.start()
