# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import pytest

from azure_iot_device.connection_string import ConnectionString

def test_parse_with_device_id():
    """Correctly parses a connection string with a device id"""
    test_string = "Hostname=host.name;DeviceId=device;SharedAccessKey=key"
    conn_str = ConnectionString.parse(test_string)
    assert conn_str.hostname == "host.name"
    assert conn_str.device_id == "device"
    assert conn_str.shared_access_key == "key"
    assert conn_str.shared_access_key_name is None


def test_parse_with_shared_access_key_name():
    """Correctly parses a connection string with a shared access key name"""
    test_string = "Hostname=host.name;DeviceId=device;SharedAccessKeyName=keyname;SharedAccessKey=key"
    conn_str = ConnectionString.parse(test_string)
    assert conn_str.hostname == "host.name"
    assert conn_str.device_id == "device"
    assert conn_str.shared_access_key == "key"
    assert conn_str.shared_access_key_name == "keyname"

def test_parse_missing_device_id_raises_value_error():
    """Raises a ValueError if the connection string is incomplete"""
    test_string = "Hostname=host.name;SharedAccessKey=key"
    with pytest.raises(ValueError):
        ConnectionString.parse(test_string)

def test_parse_missing_hostname_raises_value_error():
    """Raises a ValueError if the connection string is incomplete"""
    test_string = "DevjceId=device;SharedAccessKey=key"
    with pytest.raises(ValueError):
        ConnectionString.parse(test_string)

def test_parse_missing_shared_access_key_raises_value_error():
    """Raises a ValueError if the connection string is incomplete"""
    test_string = "Hostname=host.name;DeviceId=device"
    with pytest.raises(ValueError):
        ConnectionString.parse(test_string)
