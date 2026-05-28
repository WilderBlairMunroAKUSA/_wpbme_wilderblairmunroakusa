#![no_std]
"""
DO:
	- stab at nospace noindented json string regex alternative...mandatory (avoid needing to write decoder object hooks for load-dump normalize preproces roundtrip.
	- bracket inconsistency in condensed form, ? ([[(), .. ()]], maybe.
	- initialize std::*
function: regex brute force convert non-primitive json text to tape array
"""
def regextapifyjson(jsonsource) -> str:
	import os
	import re
	import json
	try: # first force json structure into by-line serialized format
		if (isinstance(jsonsource, (dict, list))):
			jsont = json.dumps(jsonsource, ensure_ascii=False, indent=2)
		elif (isinstance(jsonsource, str)
			and jsonsource.lower().endswith('.json')
			and os.path.exists(jsonsource)):
			with open(jsonsource, 'r', encoding='utf-8') as f:
				jsont = json.dumps(json.load(f), ensure_ascii=False, indent=2)
		elif (isinstance(jsonsource, str)):
		   jsont = json.dumps(json.loads(jsonsource), ensure_ascii=False, indent=2)
	except:
		return ValueError("expects non-primitive json source")
		
	pattern_pairs = [	\
(r'(\s*)\{(\s*)$',								r'\1[{},\2'),					\
(r'^(\s*)\},?(\s*)$',							r'\1{}], []],\2'),				\
(r'(\s*)\[(\s*)$',								r'\1[[],\2'),					\
(r'^(\s*)\],?(\s*)$',							r'\1[]], []],\2'),				\
(r'(".*"): (".*"),?\s*$',						r'[[], [\1: \2]],'),			\
(r'^(\s*)(\{\}|\[\]|.*[^,\s\]\}]),?(\s*)$',		r'\1[[], [\2]],\3'),			\
(r'(".*"): (\{\}|\[\]),?\s*$',					r'[[], [\1: \2]],'),			\
(r'(".*"): \[(\{\}|\[\]),\s*$',					r'[[{}, [\1]], [\2,'),			\
(r'\[\[\], \[(".*[^\\]"): (.*)\]\]',			r'[[{}, [\1]], [[\2], []]]'),	\
(r'^(\s*)\[(\{\}|\[\]),\s*$',					r'\1[[], [\2,')					\
]
	for pair in pattern_pairs:
		jsont = re.sub(pair[0], pair[1], jsont, flags=re.MULTILINE)
	jsont = jsont[:-1]		# pop trailing comma
	return jsont
	
def jsontapewind(tapifiedjson) -> str:
	import re
	import json

	jsonr = tapifiedjson
	pattern_pairs = [	\
(r'\[\[\{\}, \[(.*)\]\], \[\[(.*)\], \[\]\]\],',r'[\1, [\2]],'),				\
(r'\[\[\{\}, \[(.*)\]\], \[(\[\]|\{\}),',		r'[\1, [\2,'),					\
(r'^(\s*)(\[\]|\{\})\], \[\]\],(\s*)$',			r'\1\2]],\3'),					\
(r'^(\s*)\[\[\], \[(\[\]|\{\}),(\s*)$',			r'\1[[\2,\3'),					\
(r'^(\s*)\[\[\], \[(.*)\]\],(\s*)$',			r'\1[\2],\3'),					\
(r'^(\[\]|\{\})\], \[\]\](\s*)$',				r'\1]]\2')						\
]
	for pair in pattern_pairs:
		jsonr = re.sub(pair[0], pair[1], jsonr, flags=re.MULTILINE)
	return jsonr
