# coding: utf-8


class Rule:
    """
    Rule Object used to represent DB Rules received from Database
    """
    def __init__(self, topic, operator="!=", equated=""):
        self._topic = topic
        self._operator = operator
        self._equated = equated

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic_name):
        self._topic = topic_name

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, operator_type):
        self._operator = operator_type

    @property
    def equated(self):
        return self._equated

    @equated.setter
    def equated(self, equated_value):
        self._equated = equated_value

    def __str__(self):
        return f'{self.topic} {self.operator} {self.equated}'


class HomieRule:
    """
    Rule object based in the protocol MQTT using the Homie Convention
    """
    def __init__(self, device_id, node, property_name):
        self.device_id = device_id
        self.node = node
        self.property_name = property_name

        self.operator = '!='
        self.equated = ''
        self.topic = (
            f'homie/{self.device_id}/{self.node}/{self.property_name}' or
            ''
        )

    def set_operation(self, operator, equated):
        self.operator = operator or '!='
        self.equated = equated or ''

    def __str__(self):
        return f'{self.topic}, {self.operation}, {self.equated}'
