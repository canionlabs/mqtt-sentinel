# coding: utf-8
import paho.mqtt.client as mqtt


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
    def __init__():
        """
        """
        pass

    def config():
        """
        Create a MQTTClient using a config file
        """
        pass
