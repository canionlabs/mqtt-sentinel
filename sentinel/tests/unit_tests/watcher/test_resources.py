from sentinel.rules import RuleDBObject
from sentinel.watcher import WatcherPool, WatcherWorker, MQTTWatcher

from unittest.mock import Mock

import paho.mqtt.client as mqttc
import pytest

import uuid


@pytest.fixture
def mqtt_rule():
    rule = RuleDBObject(topic=str(uuid.uuid4()), operator="!=", equated="")
    return rule


# @pytest.fixture
# def mqtt_watcher():
#     rule = RuleDBObject(topic=str(uuid.uuid4()), operator="!=", equated="")
#     watcher = MQTTWatcher()
#     watcher.watch_rule(rule)
#     return watcher


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
    worker = WatcherWorker()
    worker.connect('localhost', 1883, 60)
    worker.start()
    worker.add_rule(mqtt_rule)
    mock_mqttc.loop_stop.assert_called_with()
    mock_mqttc.subscribe.assert_called_once_with(mqtt_rule.topic)
    mock_mqttc.loop_start.assert_called_with()


def test_worker_availability(monkeypatch, mock_mqttc, mqtt_rule):
    MQTT_MOCK = Mock(return_value=mock_mqttc)
    monkeypatch.setattr(
        'paho.mqtt.client.Client', MQTT_MOCK
    )
    worker = WatcherWorker()
    worker.connect('localhost', 1883, 60)
    worker.start()
    for i in range(1, 15):
        mqtt_rule.topic = str(uuid.uuid4())
        worker.add_rule(mqtt_rule)
        if i < 10:
            assert worker.is_avaliable()
        else:
            assert not worker.is_avaliable()


# def test_pool_creation(monkeypatch):
#     Mock



# def test_watcher_worker_mocker(mocker):
#     with mocker.patch()

    # with mocker.patch('sentinel.watcher.workers.paho.mqtt.client.Client') as paho_mocker:
    #     host = 'localhost'
    #     port = 1883
    #     keepalive = 60
    #     paho_mocker.return_value.connect.return_value = "teste"
    #     import pdb; pdb.set_trace()
    #     # paho_mocker.return_value = helpers.init_mock_mqtt()

    #     watcher = WatcherWorker()
    #     watcher.connect(host, port, keepalive)
    #     watcher.start()
    # import pdb; pdb.set_trace()
    # paho_mocker.connect.assert_called_with()


# def test_mqtt_watcher_rule(mqtt_rule, mocker):
#     with mocker.patch('sentinel.watcher.WatcherPool') as pool_mock:
#         watcher = MQTTWatcher()
#         pool_mock.acquire.return_value = True
#         watcher.watch_rule(mqtt_rule)
#         # pool_mock.acquire.assert_called_with()

#     # pool = watcher._pool
#     # assert isinstance(pool, WatcherPool)
#     # assert len(pool._worker_list) >= 1


# def test_mqtt_watcher_worker_subscribe_topic(mqtt_rule):
#     watcher = MQTTWatcher()
#     watcher.watch_rule(mqtt_rule)

#     worker_list = watcher._pool._worker_list
#     for worker in worker_list:
#         assert mqtt_rule.topic in worker.subscribed_topics


# def test_mqtt_watcher_worker_is_avaliable(mqtt_watcher):
#     worker_list = mqtt_watcher._pool._worker_list
#     for worker in worker_list:
#         assert worker.is_avaliable
