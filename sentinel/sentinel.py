# coding: utf-8
import logging

from sentinel.database import manager
from sentinel.watcher import Watcher
from sentinel import settings


class Sentinel:
    def __init__(self, host='localhost', port=1883, keepalive=60):
        self.db = None
        self.watcher = Watcher(host, port, keepalive)

    def set_mqtt_auth(self, username, password):
        self.watcher.set_auth(username, password)

    def set_output(self, output_service):
        settings.output_service = output_service

    def set_db(self, db_url='sqlite://sentinel.db'):
        self.db = manager(db_url)
        self.db.migrate()
        settings.db_service = self.db

    def add_rule(self, mqtt_rule):
        if not self.db.this_rule_exists(mqtt_rule):
            self.db.add_rule(mqtt_rule)
        else:
            logging.warning('This rule already exists')

    def start(self):
        self._checkup()
        self.watcher.run()

    def _checkup(self):
        if not settings.output_service:
            raise NameError("Output service is not found")
        if not settings.db_service:
            raise NameError("DB service is not found")
