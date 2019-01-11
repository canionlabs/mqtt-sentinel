# coding: utf-8
import paho.mqtt.publish as publish


class OutMQTT:
    def __init__(self, host='localhost', port=1883,
                 topic='notifications/', qos=0,
                 username='', password=''):
        self.host = host
        self.port = port
        self.topic = topic
        self.qos = qos
        self.auth = {
            'username': username,
            'password': password
        }

    def publish(self, payload):
        if self.auth['username']:
            publish.single(
                topic=self.topic, payload=payload,
                qos=self.qos, hostname=self.host, auth=self.auth
            )
        else:
            publish.single(
                topic=self.topic, payload=payload,
                qos=self.qos, hostname=self.host
            )

    def send(self, mqtt_msg, rule):
        payload_msg = (
            f"The value {mqtt_msg.payload} has been received in the" +
            f"topic {mqtt_msg.topic}. " +
            f"Rule: value {rule.operator} {rule.equated}"
        )
        self.publish(payload_msg)
