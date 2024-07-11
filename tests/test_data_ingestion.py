import sys
import os

# Add the project root to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import Mock, patch
from backend.ingestion.data_ingestion import on_connect, on_message

# Mock InfluxDB write API
write_api_mock = Mock()

# Test on_connect function
def test_on_connect():
    client = Mock()
    userdata = None
    flags = None
    rc = 0

    with patch('builtins.print') as mocked_print:
        on_connect(client, userdata, flags, rc)
        mocked_print.assert_called_with("Connected with result code 0")

# Test on_message function
def test_on_message():
    client = Mock()
    userdata = None
    msg = Mock()
    msg.payload.decode.return_value = '1629212345,75'

    with patch('backend.ingestion.data_ingestion.write_api.write') as write_api_mock:
        on_message(client, userdata, msg)
        write_api_mock.assert_called_once()

        args, kwargs = write_api_mock.call_args
        assert kwargs['bucket'] == 'sleep_tracker'
        assert kwargs['org'] == 'None'
        point = kwargs['record']
        assert point['measurement'] == 'heart_rate'
        assert point['tags'] == {'user_id': 'user1'}
        assert point['fields'] == {'value': 75}
