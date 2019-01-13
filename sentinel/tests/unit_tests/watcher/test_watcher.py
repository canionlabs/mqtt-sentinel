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
