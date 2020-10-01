###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from autobahn.twisted.component import Component, run
from autobahn.twisted.util import sleep
from twisted.internet.defer import inlineCallbacks
import os
import argparse
import json
from datetime import datetime
from twisted.internet import task, reactor


# parser = argparse.ArgumentParser(description='Devices prototype')
# parser.add_argument('-i', '--id', default=1, help='DeviceId')
# args = parser.parse_args()


url = os.environ.get('CBURL', 'ws://localhost:8080/ws')
realmvalue = os.environ.get('CBREALM', 'realm1')
topic = os.environ.get('CBTOPIC', 'com.myapp.hello')
component = Component(transports=url, realm=realmvalue)

device_id = "2"
save_session = None
save_detail = None


@component.on_join
@inlineCallbacks
def joined(session, details):
    global save_session
    global save_detail
    save_session = session
    save_detail = details

    print("session ready")
    print(f"Device id:{device_id}")

    # Function for remote calling
    def utcnow(device_id, prc_call_id):
        print(f"Recived RPC from device {device_id}")
        now = datetime.utcnow()
        #res = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        res = (f"Do PRC:{prc_call_id}")
        print(res)
        return res

    try:
        yield session.register(utcnow, 'my.com.date')
        print("procedure registered")
    except Exception as e:
        print("could not register procedure: {0}".format(e))

    # Function run when recive message

    def oncounter(message):
        print("Recived new rule.")

    try:
        yield session.subscribe(oncounter, topic)
        print("subscribed to topic")
    except Exception as e:
        print("could not subscribe to topic: {0}".format(e))


if __name__ == "__main__":
    run([component])
