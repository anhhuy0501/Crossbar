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
import time


# parser = argparse.ArgumentParser(description='Devices prototype')
# parser.add_argument('-i', '--id', default=1, help='DeviceId')
# args = parser.parse_args()


url = os.environ.get('CBURL', 'ws://localhost:8080/ws')
realmvalue = os.environ.get('CBREALM', 'realm1')
topic = os.environ.get('CBTOPIC', 'com.myapp.hello')
component = Component(transports=url, realm=realmvalue)

device_id = "1"
save_session = None
save_detail = None

prc_call_id = 1


def schedule_work(interval):
    global prc_call_id
    time.sleep(interval)

    try:
        print(f"Call RPC id: {prc_call_id}")
        res = save_session.call('my.com.date', device_id, prc_call_id)
        #print("\ncall result: {}\n".format(res))
    except Exception as e:
        print("call error: {0}".format(e))

    # set new call_id
    prc_call_id += 1

# Function run when recive message


def oncounter(message):
    # Convert to dict
    rules = json.loads(message)
    print(f"New interval: {rules[0]['interval']}")
    # Check rules
    for rule in rules:
        schedule_work(rule["interval"])


@component.on_join
@inlineCallbacks
def joined(session, details):
    global save_session
    global save_detail
    save_session = session
    save_detail = details

    print("session ready")
    print(f"Device id: {device_id}")

    try:
        session.subscribe(oncounter, topic)
        print("subscribed to topic")
    except Exception as e:
        print("could not subscribe to topic: {0}".format(e))

    yield 0

    # yield perodic_work()


if __name__ == "__main__":
    run([component])
