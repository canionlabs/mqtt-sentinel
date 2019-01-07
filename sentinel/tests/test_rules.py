# coding: utf-8
from sentinel.rules import HomieRule

import pytest

import random
import uuid


@pytest.fixture("module")
def homie_info(request):
    return {
        "device_id": str(uuid.uuid4()),
        "node": str(uuid.uuid4()),
        "property_name": str(uuid.uuid4())
    }


def test_rule_represetation(homie_info):
    operator_type = ">="
    equated_value = str(random.randint(1, 10000))
    homie_rule = HomieRule(**homie_info)
    homie_rule.set_operation(operator_type, equated_value)

    assert homie_rule.topic == (
        f"homie/{homie_info['device_id']}" +
        f"/{homie_info['node']}/{homie_info['property_name']}"
    )
    assert homie_rule.operator == operator_type
    assert homie_rule.equated == equated_value
