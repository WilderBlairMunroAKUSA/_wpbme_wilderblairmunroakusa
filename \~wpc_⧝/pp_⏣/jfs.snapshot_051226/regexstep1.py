#![no_std]
"""
function: regex brute force convert non-primitive json text to json array
input: non-primitive json text or structure						
operation:
. normalize serialized json text, fully expanded by line
. perform regex substitutions to convert structueres and values to array
output: pretty form (string) and raw form (single array)
format:
. array singleton is literal value
. naked []/{} delimit singletons with array/object as zeroth & last elements
"""
def regextapifyjson(jsonsource) -> {"pretty": str, "array": list}:
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
	def tedit(jsont, matchp, replacep):
		return re.sub(matchp, replacep, jsont, flags=re.MULTILINE)
	
	jsont_raw = jsont
	
	jsont = tedit(jsont,	# object open, `{`->`[{}, {`
		r'(\s*)\{(\s*)$',
		r'\1[{},\2')
	jsont = tedit(jsont,	# object close, `}_`->`{}],`
		r'^(\s*)\},?(\s*)$',
		r'\1{}]},\2')	
	jsont = tedit(jsont,	# array open, `[`->`[[],`
		r'(\s*)\[(\s*)$',
		r'\1[[],\2')
	jsont = tedit(jsont,	# array close, `]_`->`[]],`
		r'^(\s*)\],?(\s*)$',
		r'\1[]]},\2')
	"""
	"""
	"""
	jsont = tedit(jsont,	# add commas to EOL
		r'([^,\s])\s*$',
		r'\1,')
	jsont = tedit(jsont,	# close objects
		r'\[\{\},',
		r'[{}, {')
	"""
	
	jsont = tedit(jsont,	# member, primitive, `"_": _`->`["_", [_]],`
		r'(".*"): (\[\]|\{\}|[^\[\{].*[^,]),?(\s*)$',
		r'{\1: \2},\3')
	
	jsont = tedit(jsont,	# member, array/object, `"_": [(),`->`["_", [(),`
		r'(".*"): \[(\{\}|\[\]),\s*$',
		r'{\1: [\2,')

	jsont = tedit(jsont,	# array primitive element, `_`->`[_],`
		r'^(\s*)(\{\}|\[\]|.*[^,\s\]\}]),?(\s*)$',
		r'\1[\2],\3')
	jsont = tedit(jsont,	# array primitive element, `_`->`[_],`
		r'^(\s*)\[(\{\}|\[\]),',
		r'\1{"": [\2,')
	"""
	jsont = tedit(jsont,	# member, array/object, `"_": [(),`->`["_", [(),`
		r'(".*"): \[\[\],\s*$',
		r'[{}, [[\1], []], []')
	"""
	jsont = re.sub(r'\{"": ', '', jsont, count=1)
	jsont = jsont[:-2]		# pop trailing comma
	
	"""
	jsont_raw = jsont_raw.split("\n")
	for index, line in enumerate(jsont.split("\n")):
		print(jsont_raw[index])
		print(line)
	"""
	print(jsont)
	return {
		"pretty": jsont,
		"array": json.loads(jsont)
	}
	
