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

import sys
import time

from tintri.common import TintriServerError
from tintri.v310 import Tintri

"""
 This scripts shows all notificationPolicies (or only policies for a given alert)

 Command usage: get_notifications.py <server> <userName> <password> [<alertId>] 

"""
# For exhaustive messages on console, make it to True; otherwise keep it False
debug_mode = False
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


def print_policies():
    policies = tintri.get_alert_notification_policy(alert_id=alert_id)

    try:
        # object is iterable
        iter(policies)
    except TypeError:
        # only one result: make it iterable
        policies = (policies,)

    print("Policy Name\tEnabled\tAlert IDs")
    for policy in policies:
        print("%s\t%s\t%s\t%s" % (policy.uuid.uuid, policy.name, policy.notificationEnabled, ','.join(policy.alertIds)))
    pass


# main
if len(sys.argv) < 4:
    print("\nShows alert policies.\n")
    print("Usage: " + sys.argv[0] + " server user_name password [alert_id]")
    print("   Where: server    - the VMstore name or IP address")
    print("          user_name - an administrative user usually 'admin'")
    print("          password  - the password for user_name")
    print("          alert_id  - optional: only for this alert ID")
    print("")
    sys.exit(-1)

server_name = sys.argv[1]
user_name = sys.argv[2]
password = sys.argv[3]
try:
    alert_id = sys.argv[4]
except IndexError:
    alert_id = None

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
    print_policies()

except TintriServerError as tse:
    print_error(tse.__str__())
    tintri.logout()
    sys.exit(2)

# All pau, log out
tintri.logout()
