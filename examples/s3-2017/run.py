"""
s317 run.py
"""
# NOTE: check run-local for updates
# start with sudo python run.py > log 2>&1

# test cmds:
# curl -X POST -F "cmd=pingall" localhost:5000/cli
# curl  localhost:5000/start


import io
#from contextlib import redirect_stdout
from io import TextIOWrapper, BytesIO
from cStringIO import StringIO
from subprocess import call
from time import sleep

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Node
from mininet.util import waitListening
from mininet.log import setLogLevel, info

from minicps.mcps import MiniCPS

from topo import MixTopo
from utils import IP

import sys

from flask import Flask, request, render_template, jsonify
#from flask_cors import CORS, cross_origin
from scapy.all import *
import signal
import sys
import os
import random
from multiprocessing import Process, Value
import httplib, urllib
#import requests
import subprocess
import json
import time
import datetime
from threading import Thread
#from bluetooth4LE import *
import ConfigParser
import struct
from functools import wraps

from hashlib import sha512


app = Flask(__name__)
#CORS(app)

net=1
attacker=1
running=False


def check_auth(username, password):

    ADMIN_512 = 'bf33ea356054cbac9cc9b65c475b8b7ea0a1347d1f28b8f92cf065614cc7853b4f1d66e498111aed84f8741feeda553229c970fdaec5cf60b8c00250bbdcb6cf'

    ATTACKER_512 = '56aff393533461d974487c1222171a5a6a0a6fe883c7658070ee3c38022c52a3de0d74a634a909b2eb78bd109bc830d81939033a11e7fc77b5458848264f57f3'


    if username == 'admin':

        admin_512 = sha512(password.strip()).hexdigest()
        return admin_512 == ADMIN_512

    elif username == 'attacker':

        attacker_512 = sha512(password.strip()).hexdigest()
        return attacker_512 == ATTACKER_512

    else:
        return False

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/cli', methods=['POST'])
@requires_auth
def cli():
    global net
    cmd = request.form['cmd']
    secret = request.form['secret']
    secret_512 = sha512(secret.strip()).hexdigest()

    ADMIN_512 = 'bf33ea356054cbac9cc9b65c475b8b7ea0a1347d1f28b8f92cf065614cc7853b4f1d66e498111aed84f8741feeda553229c970fdaec5cf60b8c00250bbdcb6cf'

    if secret_512 != ADMIN_512:
	return '\nPlease send secret.\n'

    with open('/tmp/webapp-cmd', 'w') as f:
        f.write(cmd)

    try:
        with open('/tmp/webapp-log', 'r') as f:
            old=f.read()
    except:
        with open('/tmp/webapp-log', 'w') as f:
            old=''

    CLI(net, script='/tmp/webapp-cmd')

    try:
        with open('/tmp/webapp-log', 'r') as f:
            new=f.read()
    except:
        with open('/tmp/webapp-log', 'w') as f:
            new=''

    return new[len(old):]


@app.route('/start')
@requires_auth
def start():

    global net, attacker, running

    if running:
        return '\nServer already running.\n'

    setLogLevel('info')

    topo = MixTopo()
    net = Mininet(topo=topo)

    s1 = net['s1']
    plc2 = net['plc2']
    plc3 = net['plc3']

    s2, rtu2a, scada = net.get('s2', 'rtu2a', 'scada')
    rtu2b, attacker2 = net.get('rtu2b', 'attacker2')
    s3 = net.get('s3')

    # NOTE: root-eth0 interface on the host
    root = Node('root', inNamespace=False)
    intf = net.addLink(root, s3).intf1
    print('DEBUG root intf: {}'.format(intf))
    root.setIP('10.0.0.30', intf=intf)
    # NOTE: all packet from root to the 10.0.0.0 network
    root.cmd('route add -net ' + '10.0.0.0' + ' dev ' + str(intf))


    net.start()
    info('Welcome')

    # NOTE: use for debugging
    #s1.cmd('tcpdump -i s1-eth1 -w /tmp/s1-eth1.pcap &')
    #s1.cmd('tcpdump -i s1-eth2 -w /tmp/s1-eth2.pcap &')

    SLEEP = 0.5

    # NOTE: swat challenge 1 and 2
    plc3.cmd(sys.executable + ' plc3.py &')
    sleep(SLEEP)
    plc2.cmd(sys.executable + ' plc2.py &')
    sleep(SLEEP)

    # NOTE: wadi challenge 1
    scada.cmd(sys.executable + ' scada.py &')
    sleep(SLEEP)
    rtu2a.cmd(sys.executable + ' rtu2a.py &')
    sleep(SLEEP)
    # NOTE: wadi challenge 2
    rtu2b.cmd(sys.executable + ' rtu2b.py &')
    sleep(SLEEP)


    running = True
    return '\nServer started.\n'

@app.route('/stop')
@requires_auth
def stop():
    global net, attacker, running

    if not running:
        return '\nServer not running.\n'


    net.stop()

    print "*** Running clean.sh"
    call('./clean.sh')

    running = False


    return '\nServer successfully stopped.\n'


@app.route('/restart')
@requires_auth
def restart():

    stop()
    start()

    return '\nServer successfully restarted.\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded = True)


