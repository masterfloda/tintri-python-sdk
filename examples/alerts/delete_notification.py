#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Tintri, Inc.
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
import re
import sys
import time

from tintri.common import TintriServerError, TintriError
from tintri.v310 import Tintri, AlertNotificationPolicy

"""
 This scripts deletes notificationPolicies by one or more policy UUIDs or alertIds

 Command usage: 
 delete_notifications.py <server> <user_name> <password> <UUIDs|alerts>

"""
# For exhaustive messages on console, make it to True; otherwise keep it False
debug_mode = True
APPLIANCE_URL = "/v310/alert/notificationPolicy"


def print_with_prefix(prefix, out):
    print(prefix + out)
    return


def print_debug(out):
    if debug_mode:
        print_with_prefix("[DEBUG] : ", out)
    return


def print_info(out):
    print_with_prefix("[INFO] : ", out)
    return


def print_error(out):
    print_with_prefix("[ERROR] : ", out)
    return


def my_timezone():
    tz_hours = time.timezone / -3600
    tz_minutes = time.timezone % 3600
    return "{0:0=+3d}:{1:0=2d}".format(tz_hours, tz_minutes)


def delete_notification_policies():
    # regex to check if an identifier is a UUID
    uuid_regex = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
    uuids = []

    # loop through the given identifiers and collect the UUIDs
    for thing in identifiers.split(','):
        if uuid_regex.match(thing):
            # it's already a UUID
            uuids.append(thing)
        else:
            # assume it's an alertId and try to get the matching policy
            try:
                policy = tintri.get_alert_notification_policy(alert_id=thing)
                uuids.append(policy[0].uuid.uuid)
            except TintriServerError:
                print_info(thing + ' not found')

    # loop through the (unique) collected UUIDs and delete each one of them
    for uuid in set(uuids):
        print_info('delete ' + uuid)
        try:
            tintri.delete_alert_notification_policy(uuid=uuid)
        except TintriError as e:
            print_error(e.cause)


# main
if len(sys.argv) < 5:
    print("\nCreates a notificationPolicy.\n")
    print("Usage: " + sys.argv[0] + " server user_name password alerts")
    print("   Where: server    - the VMstore name or IP address")
    print("          user_name - an administrative user usually 'admin'")
    print("          password  - the password for user_name")
    print("          UUIDs|alerts  - one or more UUIDs or alert IDs, comma separated")
    print("")
    sys.exit(-1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]
identifiers = sys.argv[4]

try:
    # instantiate the Tintri server.
    tintri = Tintri(server_name)

    # Get version and product
    version_info = tintri.version
    product_name = version_info.productName
    if not tintri.is_vmstore():
        raise TintriServerError(0, -1, "Tintri server needs to be VMstore, not " + product_name)

    preferredVersion = version_info.preferredVersion
    print("API Version: " + preferredVersion)

    # Login to TGC
    tintri.login(user_name, password)

except TintriServerError as tse:
    print_error(tse.__str__())
    sys.exit(2)

try:
    delete_notification_policies()

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(2)

# All pau, log out
tintri.logout()
