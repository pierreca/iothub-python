# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import time
from urllib import urlencode, quote_plus

class ConnectionString(object):
    """Represents the parameters of a device connection to an Azure IoT Hub instance"""

    def __init__(self, device_id, shared_access_key_name, shared_access_key, hostname):
        self.device_id = device_id
        self.shared_access_key_name = shared_access_key_name
        self.shared_access_key = shared_access_key
        self.hostname = hostname

    def generate_sas_token(self, expiry=None):
        """Create a shared access signiture token as a string literal.
        :returns: SAS token as string literal.
        :rtype: str
        """
        from base64 import b64encode, b64decode
        from hashlib import sha256
        from hmac import HMAC
        uri = self.hostname + "/devices/" + self.device_id
        if not expiry:
            expiry = time.time() + 3600  # Default to 1 hour.
        encoded_uri = quote_plus(uri)
        ttl = int(expiry)
        sign_key = '%s\n%d' % (encoded_uri, ttl)
        signature = b64encode(HMAC(b64decode(self.shared_access_key), sign_key.encode('utf-8'), sha256).digest())
        result = {
            'sr': uri,
            'sig': signature,
            'se': str(ttl)}
        if self.shared_access_key_name:
            result['skn'] = self.shared_access_key_name
        return 'SharedAccessSignature ' + urlencode(result)

    @staticmethod
    def parse(connection_string):
        hostname = None
        shared_access_key_name = None
        device_id = None
        shared_access_key = None
        for element in connection_string.split(';'):
            key, _, value = element.partition('=')
            if key.lower() == 'hostname':
                hostname = value.rstrip('/')
            elif key.lower() == 'sharedaccesskeyname':
                shared_access_key_name = value
            elif key.lower() == 'sharedaccesskey':
                shared_access_key = value
            elif key.lower() == 'deviceid':
                device_id = value
        if all([hostname, device_id, shared_access_key]) or all([hostname, shared_access_key_name, shared_access_key]):
            return ConnectionString(device_id, shared_access_key_name, shared_access_key, hostname)
        else:
            raise ValueError("Invalid connection string")
