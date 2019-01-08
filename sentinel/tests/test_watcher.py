from sentinel.rules import RuleDBObject
from sentinel.watcher import MQTTWatcher, WatcherPool

import pytest

import uuid


@pytest.fixture
def mqtt_rule():
    rule = RuleDBObject(topic=str(uuid.uuid4()), operator="!=", equated="")
    return rule


@pytest.fixture
def mqtt_watcher():
    rule = RuleDBObject(topic=str(uuid.uuid4()), operator="!=", equated="")
    watcher = MQTTWatcher()
    watcher.watch_rule(rule)
    return watcher


def test_mqtt_watcher_rule(mqtt_rule):
    watcher = MQTTWatcher()
    watcher.watch_rule(mqtt_rule)

    pool = watcher._pool
    assert isinstance(pool, WatcherPool)
    assert len(pool._worker_list) >= 1


def test_mqtt_watcher_worker_subscribe_topic(mqtt_rule):
    watcher = MQTTWatcher()
    watcher.watch_rule(mqtt_rule)

    worker_list = watcher._pool._worker_list
    for worker in worker_list:
        assert mqtt_rule.topic in worker.subscribed_topics


def test_mqtt_watcher_worker_is_avaliable(mqtt_watcher):
    worker_list = mqtt_watcher._pool._worker_list
    for worker in worker_list:
        assert worker.is_avaliable
