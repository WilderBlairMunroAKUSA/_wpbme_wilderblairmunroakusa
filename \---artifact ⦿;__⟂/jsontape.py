#![no_std]

import os, re, json
from collections import deque

# magics map:
DEL								= 0x7F
COM, COL, DQ_					= ',', ':', '"'
CB_, _CB, SB_, _SB				= '{', '}', '[', ']'
AB_, _AB						= '<', '>'

NUL_STR, NUL_PRI				= '',  '||'
NUL_OBJ, NUL_ARR, NUL_MEM		= CB_+_CB, SB_+_SB, AB_+_AB		# {}, [], <>
NULL, TRUE, FALSE				= 'null',  'true',  'false'

VS,  VS_START,  VS_END			= 0xFE00,  0xFE00,  0xFE0F
VSP, VSP_START, VSP_END			= 0xE0100, 0xE0100, 0xE01EF
TAG, TAG_START, TAG_END			= 0xE0000, 0xE0020, 0XE007F

OBJ_TYP							= DQ_+AB_+NUL_OBJ+_AB+DQ_		# "<{}>"
ARR_TYP							= DQ_+AB_+NUL_ARR+_AB+DQ_		# "<[]>"
PRI_TYP							= DQ_+AB_+NUL_PRI+_AB+DQ_		# "<||>"
MEM_TYP							= DQ_+AB_+NUL_MEM+_AB+DQ_		# "<<>>"

TOK_OBJ_O, TAG_OBJ_O			= SB_+OBJ_TYP+COM+SB_, TAG+0x7B	# ["<{}>",[
TOK_OBJ_C, TAG_OBJ_C			= _SB+COM+OBJ_TYP+_SB, TAG+0x7D	# ],"<{}>"]
TOK_ARR_O, TAG_ARR_O			= SB_+ARR_TYP+COM+SB_, TAG+0x5B	# ["<[]>",[
TOK_ARR_C, TAG_ARR_C			= _SB+COM+ARR_TYP+_SB, TAG+0x5D	# ],"<[]>"]
TOK_PRI_O, TAG_PRI_O			= SB_+PRI_TYP+COM+SB_, TAG+0x7C	# ["<||>",[
TOK_PRI_C, TAG_PRI_C			= _SB+COM+PRI_TYP+_SB, TAG+0x7C	# ],"<||>"]
TOK_MEM_O, TAG_MEM_O			= SB_+MEM_TYP+COM+SB_, TAG+0x3C	# ["<<>>",[
TOK_MEM_C, TAG_MEM_C			= _SB+COM+MEM_TYP+_SB, TAG+0x3E	# ],"<<>>"]

_OPENS			= (CB_, SB_)
_CLOSES			= (_CB, _SB)
_TOK_OPENS		= (TOK_ARR_O, TOK_OBJ_O, TOK_PRI_O, TOK_MEM_O)
_TOK_CLOSES		= (TOK_ARR_C, TOK_OBJ_C, TOK_PRI_C, TOK_MEM_C)
_B96			= [chr(TAG_START + i) for i in range(96)]
_B96_INV		= {c: i for i, c in enumerate(_B96)}

MINIFIED = re.compile(r'''
	("(?:\\.|[^"\\])*")|\s+
	''', re.VERBOSE)
JSON_PRIMITIVE = re.compile(r'''
	^(?:"(?:\\.|[^"\\])*"
	|	-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?
	|	true|false|null
	)$''', re.VERBOSE)
JSON_TOKENIZE = re.compile(r'''
		"(?:\\.|[^"\\])*"
	|	-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?
	|	true|false|null
	|	[\[\]\{\}:,]
	''', re.VERBOSE)

# helper / encode/decode functions:
def vsiink_from_utf8(utf8_str):
# vsiink	:= variation selector invisible ink
# Bs		:= Bytes
	Bs = utf8_str.encode('utf-8')
	vsiink = []
	for b in Bs:
		if b < 16: vsiink.append(chr(DEL) + chr(VS_START + b))	# VS1–VS16
		else: vsiink.append(chr(VSP_START + (b - 16)))			# VS17–VS256
	return NUL_STR.join(vsiink)
def vsiink_to_utf8(vsiink_str):
	Bs = []
	for ch in vsiink_str:
		if VS_START <= ord(ch) <= VS_END:
			Bs.append(ord(ch) - VS_START)
		elif VSP_START <= ord(ch) <= VSP_END:
			Bs.append((ord(ch) - VSP_START) + 16)
	return bytes(Bs).decode('utf-8')

def b96_from_int(n):
	if n == 0: return _B96[0]
	digits = []
	while n:
		digits.append(_B96[n % 96])
		n //= 96
	return NULL_STR.join(reversed(digits))
def b96_to_int(s):
	n = 0
	for ch in s:
		n = n * 96 + _B96_INV[ch]
	return n
def json_minify(_json):
	return re.sub(MINIFIED, lambda m:
		m.group(1) if m.group(1) else NUL_STR, _json)

# json array tape/reel IR preparation functions:
def json_text_coerce(_json):
	if _json is None: return NULL
	if isinstance(_json, bool): return TRUE if _json else FALSE
	if isinstance(_json, (int, float)):
		return json.dumps(_json)
	if isinstance(_json, (dict, list)):
		return json_minify(json.dumps(_json, ensure_ascii=False))
	if isinstance(_json, str):
		if _json.endswith('.json') and os.path.exists(_json):
			with open(_json, 'r', encoding='utf-8') as f:
				raw = f.read()
			try:
				json.loads(raw)
				return json_minify(raw)
			except json.JSONDecodeError: pass
			if JSON_PRIMITIVE.match(raw.strip()):
				return stripped
			raise ValueError(f"{_json!r} invalid json text")
		try:
			json.loads(_json)
			return json_minify(_json)
		except json.JSONDecodeError: pass
		if JSON_PRIMITIVE.match(_json):
			return _json
		return json.dumps(_json)

def json_tape_spot(_json):
	json_text = json_text_coerce(_json)
	if json_text[0] == SB_:
		return [TOK_ARR_O, json_text, TOK_ARR_C]
	elif json_text[0] == CB_:
		return [TOK_OBJ_O, json_text, TOK_OBJ_C]
	else: return [TOK_PRI_O, json_text, TOK_PRI_C]

def member_spot(key: str, value: str):
	key_tape = json_tape(key)
	value_tape = json_tape(value)
	return TOK_MEM_O + COM.join([key_tape, value_tape]) + TOK_MEM_C

def json_tape(_json):
	_spot = json_tape_spot(_json)
	if _spot[0] == TOK_PRI_O:
		return NUL_STR.join(_spot)
	elif _spot[0] == TOK_ARR_O:
		arr_content = _spot[1][1:-1].strip()
		if not arr_content:
			return TOK_ARR_O + NUL_ARR + TOK_ARR_C
		arr_elements = split_json_array(arr_content)
		encoded_elements = [json_tape(item) for item in arr_elements]
		return TOK_ARR_O + COM.join(
			encoded_elements) + TOK_ARR_C
	elif _spot[0] == TOK_OBJ_O:
		obj_content = _spot[1][1:-1].strip()
		if not obj_content:
			return TOK_OBJ_O + NUL_OBJ + TOK_OBJ_C
		obj_members = split_json_object(obj_content)
		encoded_members = [member_spot(key, value)
			for key, value in obj_members]
		return TOK_OBJ_O + COM.join(encoded_members) + TOK_OBJ_C

def _split_json_tokens(content):
	tokens = JSON_TOKENIZE.findall(content)
	current_tokens = []
	depth = 0
	for token in tokens:
		if token in _OPENS:
			depth += 1
			current_tokens.append(token)
		elif token in _CLOSES:
			depth -= 1
			current_tokens.append(token)
		elif token == COM and depth == 0:
			if current_tokens:
				yield NUL_STR.join(current_tokens)
			current_tokens = []
		else: current_tokens.append(token)
	if current_tokens: yield NUL_STR.join(current_tokens)

def split_json_array(arr_content):
	return list(_split_json_tokens(arr_content))

def split_json_object(obj_content):
    members = []
    for segment in _split_json_tokens(obj_content):
        seg_tokens = JSON_TOKENIZE.findall(segment)
        colon_idx = next(i for i, t in enumerate(seg_tokens) if t == COL)
        key = NUL_STR.join(seg_tokens[:colon_idx])
        value = NUL_STR.join(seg_tokens[colon_idx+1:])
        members.append((key, value))
    return members

# encoding vsiink value payloads in json tape array IR:
def _tape_children(node, base_offset=0):
	tok_open = next((t for t in _TOK_OPENS if node.startswith(t)), None)
	if not tok_open: return []
	tok_close = _TOK_CLOSES[_TOK_OPENS.index(tok_open)]
	center_start = len(tok_open)
	center_end = len(node) - len(tok_close)
	center = node[center_start:center_end]
	if center in (NUL_ARR, NUL_OBJ): return []
	depth, start, i = 0, None, 0
	children = []
	while i < len(center):
		if center[i:].startswith(tuple(_TOK_OPENS)):
			if depth == 0: start = i
			depth += 1
		elif center[i:].startswith(tuple(_TOK_CLOSES)):
			depth -= 1
			if depth == 0 and start is not None:
				children.append(
					(center[start:i+len(tok_close)],
					base_offset + center_start + start))
				start = None
		i += 1
	return children

def _vsiink_encode_node(node, children, encoded_children=None):
	tok_open = next((t for t in _TOK_OPENS if node.startswith(t)), None)
	if not tok_open: return node
	tok_close = _TOK_CLOSES[_TOK_OPENS.index(tok_open)]
	center_start = len(tok_open)
	center_end = len(node) - len(tok_close)
	if not children:
		raw = node[center_start:center_end]
		encoded = DQ_ + vsiink_from_utf8(raw) + DQ_
		return node[:center_start] + encoded + node[center_end:]
	else:
		return node[:center_start] + COM.join(encoded_children) + node[center_end:]

def vsiink_encode_tape(tape,
	pre_hook=None,
	post_hook=None,
	traversal='depth'):
	q = deque([(tape, False, 0, 0)])
	encoded = {}
	push = q.append if traversal == 'depth' else q.appendleft
	pop  = q.pop    if traversal == 'depth' else q.popleft
	while q:
		node, visited, depth, offset = pop()
		children = _tape_children(node, offset)
		if visited:
			encoded_children = [
				encoded[c_off] for _, c_off in children
				] if children else None
			result = _vsiink_encode_node(node, children, encoded_children)
			if post_hook: result = post_hook(result, depth)
			encoded[offset] = result
		else:
			push((node, True, depth, offset))
			if pre_hook: pre_hook(node, depth)
			for child, child_offset in children:
				push((child, False, depth + 1, child_offset))
	return encoded[0]

# regexwhip tag replacement:
def tag_opcode_tape(tape):
	tape = re.sub(r'\["<\{\}>",\[', '["'+chr(TAG_OBJ_O)+'",[', tape)
	tape = re.sub(r'\],"<\{\}>"\]', '],"'+chr(TAG_OBJ_C)+'"]', tape)
	tape = re.sub(r'\["<\[\]>",\[', '["'+chr(TAG_ARR_O)+'",[', tape)
	tape = re.sub(r'\],"<\[\]>"\]', '],"'+chr(TAG_ARR_C)+'"]', tape)
	tape = re.sub(r'\["<\|\|>",\[', '["'+chr(TAG_PRI_O)+'",[', tape)
	tape = re.sub(r'\],"<\|\|>"\]', '],"'+chr(TAG_PRI_C)+'"]', tape)
	tape = re.sub(r'\["<<>>",\[', '["'+chr(TAG_MEM_O)+'",[', tape)
	tape = re.sub(r'\],"<<>>"\]', '],"'+chr(TAG_MEM_C)+'"]', tape)
	return tape

# regexwhip tag/vsiink concatenation:
def tape_to_reel(tape):
	return '["' + re.sub(r'[\[\],"]', NUL_STR, tape) + '"]'

# next todo
# . whip out primitives -> opcode & naked value (no string quote delimit)
#		8byte -> 4byte min (bool/number val) / 2byte max (string val)
# . hook regex whips into ecode_tape def
# . snag in depth and length tag data for arrays and objects (same surface?)
#	(^^dewhipify?)
# . tie sort hook whips
#...
# . rethink code conceal/reveal/self.rewrite scheme
