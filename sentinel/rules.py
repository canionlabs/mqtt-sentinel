# coding: utf-8


class RuleDBObject:
    """
    Rule Object used to represent DB Rules received from Database
    """
    def __init__(self, topic, operator="!=", equated=""):
        self.topic = topic
        self.operator = operator
        self.equated = equated


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
