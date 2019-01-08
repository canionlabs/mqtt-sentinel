# coding: utf-8
import paho.mqtt.client as paho_mqtt


class WatcherWorker:
    def __init__(self):
        self.subscribed_topics = []
        self.rules = []
        self.max_topics = 10
        self.mqtt_client = paho_mqtt.Client()
        self.mqtt_client.on_message = self.on_message

    def set_auth(self, username, password):
        self.mqtt_client.username_pw_set(username, password)

    def connect(self, host, port, keepalive):
        self.mqtt_client.connect(host, port, keepalive)

    def start(self):
        self.mqtt_client.loop_forever()

    def add_rule(self, rule):
        self.rules.append(
            {rule.topic: rule}
        )
        self._subscribe(rule.topic)

    def on_message(self, mqttc, userdata, msg):
        raise NotImplementedError()

    def is_avaliable(self):
        return len(self.subscribed_topics) >= self.max_topics

    def _subscribe(self, topic):
        self.subscribed_topics.append(str(topic))


class WatcherPool:
    def __init__(self):
        self._worker_list = []

    def _get_avaliable_worker(self):
        for worker in self._worker_list:
            if worker.is_avaliable:
                return worker
        return self._new_worker()

    def _new_worker(self):
        self._worker_list.append(WatcherWorker())
        return self._get_avaliable_worker()

    def acquire(self):
        return self._get_avaliable_worker()
