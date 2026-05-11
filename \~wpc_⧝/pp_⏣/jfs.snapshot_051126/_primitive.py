#!/usr/bin/env python3
"""DOCS EOF"""
import json
import re
import sys
from collections import Counter
from collections import OrderedDict

# API ====================


with open("_primitive.json", "r", encoding="utf-8") as f:
        _array = json.load(f)

_object = {
    "const": {
        "key": "value",
    },
}
_data = [
    "string",               # String
    123,                    # Number
    True,                   # Boolean
    None,                   # Null
    [1, 2, 3],             # Array
    {"key": "value"},       # 󠅏󠅢󠅪󠅥󠅣󠅴!
    _object,
]


OrderedDict((k_new if k == k_old else k, v) for k, v in od.items())

def parse(_input):

    for index, value in enumerate(_input):
        if isinstance(value, dict):
            _input[index] = {"object": [value]}
        elif isinstance(value, list):
            _input[index] = {"array": [value]}
        else:
            _input[index] = {"prime": [value]}

    return _input
print(json.dumps(parse(_array)))#, indent=4))
#print(parse(_object))
#print(parse(_data))
