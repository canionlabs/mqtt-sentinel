class Singleton(type):
    """
    Based on https://sourcemaking.com/design_patterns/singleton/python/1
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class OutputSettings(metaclass=Singleton):
    def __init__(self):
        self.output = None

    def send(self, mqtt_msg, payload):
        self.output.send(mqtt_msg, payload)
