# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import ssl
import logging
import types
from paho.mqtt import client as mqtt
from transitions import Machine
from azure_iot_device.connection_string import ConnectionString

class DeviceClient(object):
    """Client used to connect a device to an Azure IoT Hub instance"""

    def __init__(self, connection_string):
        self._mqtt_client = None
        self._connection_string = connection_string
        states = ["disconnected", "connecting", "connected", "disconnecting"]
        transitions = [
            {"trigger": "connect", "source": "disconnected", "dest": "connecting"},
            {"trigger": "on_connect", "source": "connecting", "dest": "connected"},
            {"trigger": "disconnect", "source": "connected", "dest": "disconnecting"},
            {"trigger": "on_disconnect", "source": "disconnecting", "dest": "disconnected"}
        ]
        self._fsm = Machine(states=states, transitions=transitions, initial="disconnected")
        self._fsm.on_enter_connecting(self._connect)
        self._fsm.on_enter_disconnecting(self._disconnect)
        self._fsm.on_enter_connected(self._emit_connection_status)
        self._fsm.on_enter_disconnected(self._emit_connection_status)

        self.on_connection_state = types.FunctionType
        self.on_c2d_message = types.FunctionType

    def _message_handler(self, client, userdata, msg):
        logging.info("message received")
        if self.on_c2d_message:
            self.on_c2d_message(msg.payload)
        else:
            logging.warn("message received but not handler attached")

    def connect(self):
        """Connects the client to an Azure IoT Hub instance"""
        logging.info("creating client")
        self._fsm.connect()

    def _connect(self):
        self._emit_connection_status()
        def on_connect(client, userdata, flags, result_code):
            logging.info("connected with result code: %s", str(result_code))
            if self.on_c2d_message:
                logging.info("attaching c2d handler")
                self._mqtt_client.on_message = self._message_handler
                self._mqtt_client.subscribe("devices/" + self._connection_string.device_id + "/messages/devicebound/#")
            self._fsm.on_connect()

        def on_disconnect(client, userdata, result_code):
            logging.info("disconnected with result code: %s", str(result_code))
            self._fsm.on_disconnect()

        def on_publish(client, userdata, mid):
            logging.info("payload published")

        self._mqtt_client = mqtt.Client(client_id=self._connection_string.device_id, protocol=mqtt.MQTTv311, clean_session=False)

        self._mqtt_client.on_connect = on_connect
        self._mqtt_client.on_disconnect = on_disconnect
        self._mqtt_client.on_publish = on_publish

        username = self._connection_string.hostname + "/" + self._connection_string.device_id
        sas_token = self._connection_string.generate_sas_token()

        logging.info("username: %s", username)
        logging.info("sas_token: %s", sas_token)

        self._mqtt_client.tls_set(ca_certs=os.environ.get("IOTHUB_ROOT_CA_CERT"), certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
        self._mqtt_client.tls_insecure_set(False)
        self._mqtt_client.username_pw_set(username=username, password=sas_token)

        logging.info("connecting")
        self._mqtt_client.connect(self._connection_string.hostname, port=8883)
        self._mqtt_client.loop_start()

    def disconnect(self):
        logging.info("disconnecting")
        self._fsm.disconnect()

    def _disconnect(self):
        self._emit_connection_status()
        self._mqtt_client.loop_stop()

    def send(self, payload):
        if self._fsm.state == "connected":
            logging.info('sending')
            self._mqtt_client.publish("devices/" + self._connection_string.device_id + "/messages/events/", payload, qos=1)
        else:
            raise StandardError("cannot send if not connected")

    def _emit_connection_status(self):
        logging.info("emit_connection_status")
        if self.on_connection_state:
            self.on_connection_state(self._fsm.state)

    @staticmethod
    def from_connection_string(connection_string):
        """Creates a device client with the specified connection string"""
        return DeviceClient(ConnectionString.parse(connection_string))
