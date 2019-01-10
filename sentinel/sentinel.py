# coding: utf-8
import paho.mqtt.client as mqtt
from sentinel.database import manager


class MQTTClient:
    def __init__(self, host, port, keepalive, username=None, password=None):
        self.host = host
        self.port = port or 1883
        self.keepalive = keepalive
        self.username = username
        self.password = password

        self._mqttc = mqtt.Client()
        self._set_credencials()

    def _set_credencials(self):
        if self.username:
            if self.password:
                self._mqttc.username_pw_set(self.username, self.password)
            else:
                self._mqttc.username_pw_set(self.username)

    def connect(self):
        self._mqttc.connect(self.host, self.port, self.keepalive)


class Sentinel:
    def __init__(self):
        self.db_url = None
        self.db = None

    def db_config(self, db_url):
        self.set_db(db_url)

    def set_db(self, db_url):
        self.db = manager(db_url)
        self.db_url = db_url
        self.db.migrate()
