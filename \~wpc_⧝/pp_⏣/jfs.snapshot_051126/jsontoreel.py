#!/usr/bin/env python3

import json
import math
import os
import re

class JSONToTapeDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		kwargs['object_pairs_hook'] = self.object_pairs_hook
		kwargs['parse_float'] = self.parse_float
		kwargs['parse_int'] = self.parse_int
		super().__init__(*args, **kwargs)
	
	@staticmethod
	def parse_float(s):
		"""Parse floats, preserving -0."""
		val = float(s)
		# Detect -0 by checking sign of zero
		if val == 0 and s.startswith('-'):
			return float('-0.0')
		return val
	
	@staticmethod
	def parse_int(s):
		"""Parse integers, preserving -0."""
		val = int(s)
		if val == 0 and s.startswith('-'):
			# Return a marker for -0
			return {'__negative_zero__': True}
		return val
	
	@staticmethod
	def object_pairs_hook(pairs):
		"""Preserve all key-value pairs as ordered list (not dict)."""
		return ('__pairs__', pairs)  # Marker to identify this in tape conversion
	
	def decode(self, s, *args, **kwargs):
		"""Decode and convert to tape format."""
		obj = super().decode(s, *args, **kwargs)
		return self.to_tape(obj)
	
	@staticmethod
	def to_tape(obj):
		"""Convert parsed JSON object to tape format."""
		
		# Check if it's our pairs marker (tuple from object_pairs_hook)
		if isinstance(obj, tuple) and len(obj) == 2 and obj[0] == '__pairs__':
			pairs = obj[1]
			members = []
			for key, value in pairs:
				member = [
					"member",
					[
						["name", ["string", [key]]],
						["element", JSONToTapeDecoder.to_tape(value)]
					]
				]
				members.append(member)
			# Wrap empty object in array: [{}]
			if not members:
				return ["value", ["object", [{}]]]
			return ["value", ["object", members]]
		
		elif isinstance(obj, list):
			elements = []
			for item in obj:
				element = [
					"element",
					JSONToTapeDecoder.to_tape(item)
				]
				elements.append(element)
			# Handle empty array: wrap in element frame
			if not elements:
				return ["value", ["array", [[]]]]
			return ["value", ["array", elements]]
		
		elif isinstance(obj, bool):
			# Handle bool before int (bool is subclass of int)
			type_label = "true" if obj else "false"
			return ["value", [type_label, [obj]]]
		
		elif isinstance(obj, dict) and '__negative_zero__' in obj:
			# -0 marker from parse_int
			return ["value", ["number", [float('-0.0')]]]
		
		elif isinstance(obj, (int, float)):
			# Regular number
			return ["value", ["number", [obj]]]
		
		elif isinstance(obj, str):
			return ["value", ["string", [obj]]]
		
		elif obj is None:
			return ["value", ["null", [None]]]
		
		else:
			raise ValueError(f"Unexpected type: {type(obj)}")

def collapse_json_whitespace(json_str, collapse_rules):
	"""Post-process JSON string to apply collapse rules via regex."""
	"""
	json_str = re.sub( # condense values
		r'\[\s*"value",\s*\[\s*(.*),\s*\[',
		r'["value", [\1, [',
		json_str
	)
	json_str = re.sub( # condense members
		r'\[\s*"member",\s*\[',
		r'["member", [',
		json_str
	)
	json_str = re.sub( # condense members
		r'\[\s*"element",\s*\[',
		r'["element", [',
		json_str
	)"""
	
	json_str = re.sub( # condense members
		r'(\s*".*",)\s*\[',
		r'\1 [',
		json_str
	)

	
	#json_str = re.sub( # condense literals
	#	r'\[\s*"(string|number|null|true|false)",\s*\[\s*(.*)\s*\]',
	#	r'["\1", [\2]]',
	#	json_str
	#)
	
	#json_str = re.sub(
	#	r'\[\s*"(string|number|null|true|false)",\s*\[',
	#	r'["\1", [',
	#	json_str
	#)


	"""
	# Collapse empty containers: [[]] and [{}]
	if collapse_rules.get("empty_containers"):
		json_str = re.sub(r'\[\s*\[\s*\]\s*\]', r'[[]]', json_str)
		json_str = re.sub(r'\[\s*\{\s*\}\s*\]', r'[{}]', json_str)
	
	# Collapse short arrays (len <= 1)
	if collapse_rules.get("short_arrays"):
		json_str = re.sub(r'\[\s*([^\[\{].*?)\s*\](?=\s*[\],}])', r'[\1]', json_str)
	"""
	return json_str


def format_tape_json(tape, indent=2, collapse_rules=None):
	"""Format tape as valid JSON with selective collapsing."""
	
	# Default collapse rules
	default_rules = {
		"type_tags": True,
		"empty_containers": True,
		"short_arrays": False,
	}
	
	rules = {**default_rules, **(collapse_rules or {})}
	
	# First, dump with full indentation
	json_str = json.dumps(tape, indent=indent)
	
	# Then apply collapse rules
	json_str = collapse_json_whitespace(json_str, rules)
	
	return json_str

collapse_rules = {
	"type_tags": True,
	"empty_containers": True,
	"short_arrays": True,
}


# Usage
raw = """[
  -0,
  [],
  {},
  [null, false, true],
  {"field": "dev"},
  {"tags": [
	"AI",
	"Sparse",
	[-1.1, 1e7],
	{
	  "key": {
		"sub1": false,
		"sub1": [],
		"sub1": -2
	  }
	}
  ]},
  {"active": true},
  {"key": {}}
]
"""

filename = "_output1.json"
filepath = os.path.join(f".", filename)

decoder = JSONToTapeDecoder()
tape = decoder.decode(raw)
#output = json.dumps(tape, cls=TapeJSONEncoder, indent=2)
#print(json.dumps(tape, indent=2))

with open(filepath, "w", encoding="utf-8") as output_file:
		output_file.write(format_tape_json(tape, collapse_rules=collapse_rules))

print(".")
