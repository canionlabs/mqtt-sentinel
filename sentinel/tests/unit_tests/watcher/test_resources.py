from sentinel.rules import Rule
from sentinel.watcher import WatcherPool, WatcherWorker

from unittest.mock import Mock

import paho.mqtt.client as mqttc
import pytest

import uuid


@pytest.fixture
def mqtt_rule():
    rule = Rule(topic=str(uuid.uuid4()), operator="!=", equated="")
    return rule


@pytest.fixture
def mock_mqttc():
    return Mock(spec=mqttc.Client())


def test_create_worker(monkeypatch, mock_mqttc):
    MQTT_MOCK = Mock(return_value=mock_mqttc)
    monkeypatch.setattr(
        'paho.mqtt.client.Client', MQTT_MOCK
    )
    host, port, keepalive = 'localhost', 1883, 60
    worker = WatcherWorker()
    worker.connect(host, port, keepalive)
    mock_mqttc.connect.assert_called_with(host, port, keepalive)
    worker.start()
    mock_mqttc.loop_start.assert_called_once_with()


def test_create_worker_and_add_a_rule(monkeypatch, mock_mqttc, mqtt_rule):
    MQTT_MOCK = Mock(return_value=mock_mqttc)
    monkeypatch.setattr(
        'paho.mqtt.client.Client', MQTT_MOCK
    )
    topic = str(uuid.uuid4())

    worker = WatcherWorker()
    worker.connect('localhost', 1883, 60)
    worker.start()
    worker.subscribe(topic)
    mock_mqttc.subscribe.assert_called_once_with(topic)
    mock_mqttc.loop_start.assert_called_with()


def test_worker_availability(monkeypatch, mock_mqttc):
    MQTT_MOCK = Mock(return_value=mock_mqttc)
    monkeypatch.setattr(
        'paho.mqtt.client.Client', MQTT_MOCK
    )
    worker = WatcherWorker()
    worker.connect('localhost', 1883, 60)
    worker.start()
    for i in range(1, 15):
        topic = str(uuid.uuid4())
        worker.subscribe(topic)
        if i < 10:
            assert worker.is_available()
        else:
            assert not worker.is_available()


def test_pool_worker_acquire():
    pool = WatcherPool()
    worker = pool.acquire()
    assert isinstance(worker, WatcherWorker)

    # Forcing worker to change availability
    worker.max_topics = -10
    new_worker = pool.acquire()
    assert id(worker) != id(new_worker)
