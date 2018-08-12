# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import logging
import os

from azure_iot_device.device_client import DeviceClient

logging.basicConfig(level=logging.INFO)

conn_str = os.environ.get("DEVICE_CONNECTION_STRING")
client = DeviceClient.from_connection_string(conn_str)

def connection_state_callback(status):
    print("connection status: " + status)
    if status == "connected":
        client.send("foo")

def c2d_handler(msg):
    print(msg)

client.on_connection_state = connection_state_callback
client.on_c2d_message = c2d_handler
client.connect()

while True:
    continue