# import pytest
# from unittest.mock import MagicMock, patch
# from mqtt_local import on_connect, mqtt_subscribers, mqtt_client
# from logger import logger

# @patch('mqttlocal.mqtt_client')
# @patch('mqttlocal.logger')
# def test_on_connect_success(mock_logger, mock_mqtt_client):
#     rc = 0  # Simulate successful connection

#     on_connect(mock_mqtt_client, None, None, rc)

#     # Check if the success log message is generated
#     mock_logger.info.assert_called_with("Connected to broker")

#     # Check if all topics are subscribed to and callbacks are added
#     for topic in mqtt_subscribers.keys():
#         mock_mqtt_client.subscribe.assert_any_call(topic)
#         mock_mqtt_client.message_callback_add.assert_any_call(topic, mqtt_subscribers[topic])

# @patch('mqttlocal.logger')
# def test_on_connect_failure(mock_logger):
#     mock_client = MagicMock()
#     rc = 1  # Simulate failed connection

#     on_connect(mock_client, None, None, rc)

#     # Check if the failure log message is generated
#     mock_logger.error.assert_called_with("Connection failed with code %d", rc)
