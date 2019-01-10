# coding: utf-8
from .resources import WatcherPool


class Watcher:
    def __init__(self):
        self._pool = WatcherPool()
        self.username = None
        self.password = None
        self.host = "localhost"
        self.port = 1883
        self.keepalive = 60

    def set_auth(self, username, password):
        self.username = username
        self.password = password

    def watch_rule(self, rule):
        worker = self._pool.acquire()
        if self.username:
            worker.set_auth(self.username, self.password)

        if not worker.rules:
            worker.connect(self.host, self.port, self.keepalive)
            worker.start()

        worker.add_rule(rule)
