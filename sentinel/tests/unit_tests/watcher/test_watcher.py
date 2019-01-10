from sentinel.watcher import Watcher
from sentinel.rules import RuleDBObject

import paho.mqtt.client as mqttc
import pytest

from unittest.mock import Mock
import uuid


CONNECT_DEFAULT_ARGS = ('localhost', 1883, 60)


@pytest.fixture
def mqtt_rule():
    rule = RuleDBObject(topic=str(uuid.uuid4()), operator="!=", equated="")
    return rule


@pytest.fixture
def watcher():
    watcher = Watcher()
    return watcher


@pytest.fixture
def mock_mqttc():
    return Mock(spec=mqttc.Client())


def test_watcher_create():
    host, port, keepalive = "localhost.test", 1882, 61
    watcher = Watcher(host, port, keepalive)
    assert (
        watcher.host == host and
        watcher.port == port and
        watcher.keepalive == keepalive
    )


def test_watcher_watch_a_rule(monkeypatch, mock_mqttc, watcher, mqtt_rule):
    MOCK_MQTT = Mock(return_value=mock_mqttc)
    monkeypatch.setattr(
        'paho.mqtt.client.Client', MOCK_MQTT
    )
    watcher.watch_rule(mqtt_rule)

    mock_mqttc.connect.assert_called_with(*CONNECT_DEFAULT_ARGS)
    mock_mqttc.loop_start.assert_called()
    mock_mqttc.loop_stop.assert_called()
    mock_mqttc.subscribe.assert_called_with(mqtt_rule.topic)


def test_watcher_watch_a_rule_with_auth(monkeypatch, mock_mqttc,
                                        watcher, mqtt_rule):
    MOCK_MQTT = Mock(return_value=mock_mqttc)
    monkeypatch.setattr(
        'paho.mqtt.client.Client', MOCK_MQTT
    )

    username, password = str(uuid.uuid4()), str(uuid.uuid4())
    watcher.set_auth(username, password)
    watcher.watch_rule(mqtt_rule)

    mock_mqttc.connect.assert_called_with(*CONNECT_DEFAULT_ARGS)
    mock_mqttc.username_pw_set.assert_called_with(username, password)
    mock_mqttc.loop_start.assert_called()
    mock_mqttc.loop_stop.assert_called()
    mock_mqttc.subscribe.assert_called_with(mqtt_rule.topic)


def test_watcher_watch_multiple_rules(monkeypatch, mock_mqttc,
                                      watcher, mqtt_rule):
    MOCK_MQTT = Mock(return_value=mock_mqttc)
    monkeypatch.setattr(
        'paho.mqtt.client.Client', MOCK_MQTT
    )

    for i in range(1, 20):
        mqtt_rule.topic = uuid.uuid4()
        watcher.watch_rule(mqtt_rule)

        mock_mqttc.loop_start.assert_called()
        mock_mqttc.loop_stop.assert_called()
        mock_mqttc.subscribe.assert_called_with(mqtt_rule.topic)
