#!/usr/bin/env python3

import json
import math
import os
import re


	



# Usage
raw = """[
  0,
  [],
  {},
  [null, false, true],
  {"field": "dev"},
  {"tags": [
	"AI",
	"Sparse",
	[-1.1, 1e7],
	{
	  "abc": null,
	  "key": {
		"sub2": false,
		"sub1": [],
		"sub3": -2
	  }
	}
  ]},
  {"active": true},
  {"key": {}}
]
"""
infile = "175-wilderblairmunroakusa-chatgpt-250908.json"
filename = "_outputregexed.json"
filepath = os.path.join(f".", filename)

with open(infile, "r", encoding="utf-8") as f:
    data = json.load(f)

raw_data = json.loads(raw)
raw_str = json.dumps(raw_data, ensure_ascii=False, indent=2)
data_str = json.dumps(data, ensure_ascii=False, indent=2)

def tapifyjson(json_str) -> str:
	json_str = re.sub(
		r'(\s*)\{(\s*)$',
		r'\1[{},\2',
		json_str,
		flags=re.MULTILINE
	)
	json_str = re.sub(
		r'^(\s*)\}(,?)(\s*)$',
		r'\1]\2\3',
		json_str,
		flags=re.MULTILINE
	)
	json_str = re.sub(
		r'(\s*)\[(\s*)$',
		r'\1[[],\2',
		json_str,
		flags=re.MULTILINE
	)
	json_str = re.sub(
		r'(\s*[^\[])\{\}(,?)(\s*)$',
		r'\1[{}]\2\3',
		json_str,
		flags=re.MULTILINE
	)
	json_str = re.sub(
		r'(\s*[^\[])\[\](,?)(\s*)$',
		r'\1[[]]\2\3',
		json_str,
		flags=re.MULTILINE
	)
	json_str = re.sub(
		r'(".*"): ([^\[].*[^,\s])(,?)$',
		r'[\1, [\2]]\3',
		json_str,
		flags=re.MULTILINE
	)
	json_str = re.sub(
		r'(".*"): \[(\{\}|\[\])',
		r'[\1, [\2',
		json_str,
		flags=re.MULTILINE
	)
	json_str = re.sub(
		r'^(\s*)(.*[^,\s\]\}])(,?)$',
		r'\1[\2]\3',
		json_str,
		flags=re.MULTILINE
	)
	return json_str


#output = json.dumps(tape, cls=TapeJSONEncoder, indent=2)
print(tapifyjson(raw_str))

with open(filepath, "w", encoding="utf-8") as output_file:
		output_file.write(tapifyjson(data_str))

print(".")
