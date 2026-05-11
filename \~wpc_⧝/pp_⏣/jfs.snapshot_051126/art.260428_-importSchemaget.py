#!/usr/bin/env python3
"""DOCS EOF"""
import json
import re
import sys
from collections import Counter

# API ====================
def summarize(obj):
    if isinstance(obj, dict): return _summarize_objects([obj])
    elif isinstance(obj, list): return _summarize_list(obj)
    else: return _leaf_type(obj)
def summarize_required(obj):
    """Same as summarize() but outputs only required (!) keys at every level."""
    return _filter_required(summarize(obj))
#========================
#========================
ALWAYS_EMPTY_EXCEPTIONS = set()
TYPE_PREFIX_CHAR1 = {"?", "!"}
TYPE_PREFIX_CHAR2 = {")"}
STR_TYPES_FAMILY = {"uuid", "json", "py"}
UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE)
JSON_STRING_START_CHARS = frozenset('[{"\'')

#########################
# Injection point for key normalization logic
def _normalize_key(k):
    if _is_uuid(k): return "uuid"
    return k
def _is_uuid(s): return isinstance(s, str) and bool(UUID_RE.match(s))
#########################
#

#########################
def _is_nested(v): return isinstance(v, dict)
def _is_prefix_char1(ch): return ch in TYPE_PREFIX_CHAR1
def _is_prefix_char2(ch): return ch in TYPE_PREFIX_CHAR2
#========================
"""Preserve array shape while recording schema."""
def _as_array_schema(item_schema, maxlen):
    return { "_maxlen": maxlen, "_items": item_schema, }
def _as_nested_list_schema(schema, maxlen):
    return { "_maxlen": maxlen, "_items": schema, }
#========================
def _check_serialized_string_type(s):
    """Classify string payloads that themselves encode structured data.
    Treated as atomic semantic leaf types, not recursively expanded."""
    if not isinstance(s, str): return None
    stripped = s.strip()
    if not stripped or stripped[0] not in JSON_STRING_START_CHARS: return None
    try:    # Strict JSON first.
        parsed = json.loads(stripped)
        if isinstance(parsed, (dict, list)):
            return "json"
    except Exception: pass
    # Fallback for common Python-literal-ish payloads like ['foo'].
    try:
        import ast
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            parsed = ast.literal_eval(stripped)
        if isinstance(parsed, (dict, list)):
            return "py"
    except Exception: pass
    return None
#========================
def _check_type(v):
    """Extension point for custom semantic types."""
    if isinstance(v, str) and _is_uuid(v): return "uuid"
    if isinstance(v, str):
        serialized_type = _check_serialized_string_type(v)
        if serialized_type is not None:
            return serialized_type
    return None
#========================
def _normalize_primitive_union(types):
    """Normalize primitive unions for readability and stable formatting.
    String-family unions collapse to pipe form, e.g. str|uuid.
    Other unions remain ordered lists."""
    unique = []
    for t in types:
        if t not in unique:unique.append(t)
    string_family = {"str", *STR_TYPES_FAMILY}
    if unique and all(t in string_family for t in unique):
        ordered = []
        if "str" in unique: ordered.append("str")
        ordered.extend(sorted(t for t in unique if t != "str"))
        return "|".join(ordered)
    return sorted(unique)
#========================
def _leaf_type(v):
    checked = _check_type(v)
    if checked is not None: return checked
    return type(v).__name__
#========================
def _schema_size(v):
    """Approximate structural size for readability ordering."""
    if not isinstance(v, dict): return 0
    return sum(1 for k in v if k != "_maxlen")
#========================
def _sort_keys(merged, required=frozenset()):
    """Order: required simple, optional simple, required nested, optional nested.
    Nested entries are ordered from smaller schema to larger schema."""
    req_simple = [k for k, v in merged.items() if k in required and not _is_nested(v)]
    opt_simple = [k for k, v in merged.items() if k not in required and not _is_nested(v)]
    req_nested = sorted(
        [k for k, v in merged.items() if k in required and _is_nested(v)],
        key=lambda k: (_schema_size(merged[k])))
    opt_nested = sorted(
        [k for k, v in merged.items() if k not in required and _is_nested(v)],
        key=lambda k: (_schema_size(merged[k])))
    return req_simple + opt_simple + req_nested + opt_nested
#========================
def _is_prefix_token(token):
    return (
        isinstance(token, str)
        and len(token) == 2
        and _is_prefix_char1(token[0])
        and _is_prefix_char2(token[1]))
#========================
def _split_prefixes(key):
    prefixes = []
    while len(key) >= 2 and _is_prefix_token(key[:2]):
        prefixes.append(key[:2])
        key = key[2:]
    return prefixes, key
#========================
def _bare_key(key):
    _, bare = _split_prefixes(key)
    return bare
#========================
def _join_prefixes(prefixes, bare_key):
    return "".join(prefixes) + bare_key
#========================
def _prefix_process(prefixes, bare_key, context=None):
    """Injection point for arbitrary prefix processing/composition logic."""
    return prefixes, bare_key
#========================
def _prepend_prefix(prefix, key, context=None):
    prefixes, bare_key = _split_prefixes(key)
    prefixes = [prefix] + prefixes
    prefixes, bare_key = _prefix_process(prefixes, bare_key, context=context)
    return _join_prefixes(prefixes, bare_key)
#========================
def _prefix_key(k, required):
    prefix = "!)" if k in required else "?)"
    return _prepend_prefix(prefix, k)
#========================
def _is_effectively_empty_schema(k, v):
    if k in ALWAYS_EMPTY_EXCEPTIONS: return False
    if v == "NoneType": return True
    if v == []: return True
    if v == {}: return True
    return False
#========================
def _is_required(k, cnt, total, merged):
    if k != "uuid" and _is_effectively_empty_schema(k, merged.get(k)): return False
    return cnt == total or k == "uuid"
#========================
def _build_result(merged, required, maxlen=None):
    """Assemble final dict, ordered: _maxlen?, simple fields, nested fields."""
    ordered_keys = _sort_keys(merged, required)
    result = {}
    if maxlen is not None:
        result["_maxlen"] = maxlen
    for k in ordered_keys:
        result[_prefix_key(k, required)] = merged[k]
    return result
#========================
def _merge_schemas(a, b):
    if a is None: return b
    if b is None: return a
    if isinstance(a, dict) and isinstance(b, dict):
        result = dict(a)
        for k, v in b.items():
            if k == "_maxlen":
                result["_maxlen"] = max(a.get("_maxlen", 0), b.get("_maxlen", 0))
            elif k == "_required": pass
            elif k not in result: result[k] = v
            else: result[k] = _merge_schemas(result[k], v)
        return result
    if isinstance(a, dict): return a
    if isinstance(b, dict): return b
    if isinstance(a, list) and isinstance(b, list):
        merged = list(a)
        for item in b:
            if item not in merged:
                merged.append(item)
        return merged
    if isinstance(a, list): return a if b in a else a + [b]
    if isinstance(b, list): return b if a in b else [a] + b
    if a == "NoneType": return b
    if b == "NoneType": return a
    if a == b: return a
    return [a, b]
#========================
def _summarize_objects(instances):
    if not instances: return {}
    key_counts = Counter()
    values_per_key = {}
    for inst in instances:
        if not isinstance(inst, dict):
            continue
        for k, v in inst.items():
            nk = _normalize_key(k)
            key_counts[nk] += 1
            values_per_key.setdefault(nk, []).append(v)
    total = len(instances)
    merged = {}
    for nk, vals in values_per_key.items():
        obj_vals  = [v for v in vals if isinstance(v, dict)]
        list_vals = [v for v in vals if isinstance(v, list)]
        prim_vals = [v for v in vals if not isinstance(v, (dict, list))]
        if obj_vals: merged[nk] = _summarize_objects(obj_vals)
        elif list_vals:
            true_maxlen = max(len(l) for l in list_vals)
            has_nested_lists = any(isinstance(item, list) for l in list_vals for item in l)
            if has_nested_lists:
                merged_schema = None
                for l in list_vals:
                    schema = _summarize_list(l)
                    merged_schema = schema if merged_schema is None else _merge_schemas(merged_schema, schema)
                if isinstance(merged_schema, dict) and "_maxlen" in merged_schema:
                    merged_schema["_maxlen"] = true_maxlen
                    merged[nk] = merged_schema
                else:
                    merged[nk] = _as_nested_list_schema(merged_schema, true_maxlen) if merged_schema is not None else []
            else:
                all_items = [item for l in list_vals for item in l]
                result = _summarize_list(all_items) if all_items else []
                if isinstance(result, dict) and "_maxlen" in result:
                    result["_maxlen"] = true_maxlen
                merged[nk] = result
        else:
            types = list({_leaf_type(v) for v in prim_vals if v is not None})
            if not types: merged[nk] = "NoneType"
            elif len(types) == 1: merged[nk] = types[0]
            else: merged[nk] = _normalize_primitive_union(types)
    required = {k for k, cnt in key_counts.items() if _is_required(k, cnt, total, merged)}
    return _build_result(merged, required)
#========================
def _summarize_list(obj):
    instances = [i for i in obj if isinstance(i, dict)]
    if instances:
        key_counts = Counter(
            nk
            for inst in instances
            for nk in (_normalize_key(k) for k in inst))
        total = len(instances)
        body = _summarize_objects(instances)
        clean_body = {    # strip 2char prefixes
            _bare_key(k): v
            for k, v in body.items()
            if k != "_maxlen"}
        required = {    # determine rerquired keys
            k for k, cnt in key_counts.items()
            if _is_required(k, cnt, total, clean_body)}
        return _build_result(clean_body, required, maxlen=len(obj))
    list_items = [i for i in obj if isinstance(i, list)]
    if list_items:
        true_maxlen = max(len(l) for l in list_items)
        # If this list mixes nested lists with atomic values (including json strings),
        # preserve the actual outer list shape and merge item schemas at the row/cell level
        # without expanding serialized string payloads.
        if len(list_items) != len(obj):
            item_schemas = [_summarize_list(i) if isinstance(i, list) else _leaf_type(i) for i in obj]
            merged_schema = None
            for schema in item_schemas:
                merged_schema = schema if merged_schema is None else _merge_schemas(merged_schema, schema)
            return _as_array_schema(merged_schema, len(obj))
        merged_schema = None
        for l in list_items:
            schema = _summarize_list(l)
            merged_schema = schema if merged_schema is None else _merge_schemas(merged_schema, schema)
        return _as_nested_list_schema(merged_schema, true_maxlen) if merged_schema is not None else []
    types = list({_leaf_type(i) for i in obj})
    if len(types) > 1: item_schema = _normalize_primitive_union(types)
    else: item_schema = types[0] if types else []
    return _as_array_schema(item_schema, len(obj))
#========================
def _filter_required(obj):
    """Recursively strip all ?) keys, keeping !) keys plus structural metadata."""
    if isinstance(obj, dict):
        return {
            k: _filter_required(v)
            for k, v in obj.items()
            if k in {"_maxlen", "_items"} or k.startswith("!)")}
    return obj
#========================


#========================
#========================
#========================

import os
os.makedirs(f"_conversations_schema", exist_ok=True)
# XAI ================
with open("_import_conversations🔒/_conversations_xai.json", "r", encoding="utf-8") as f:
        conversations = json.load(f)
schema = summarize(conversations)   
filename = "schema_xai_full.json"
filepath = os.path.join(f"_conversations_schema", filename)
with open(filepath, "w", encoding="utf-8") as output_file:
        json.dump(schema, output_file, ensure_ascii=False, indent=4)
schema_required = summarize_required(conversations) 
filename = "schema_xai_required.json"
filepath = os.path.join(f"_conversations_schema", filename)
with open(filepath, "w", encoding="utf-8") as output_file:
        json.dump(schema_required, output_file, ensure_ascii=False, indent=4)

# ANTHROPIC ================
with open("_import_conversations🔒/_conversations_anthropic.json", "r", encoding="utf-8") as f:
        conversations = json.load(f)
schema = summarize(conversations)
filename = "schema_anthropic_full.json"
filepath = os.path.join(f"_conversations_schema", filename)
with open(filepath, "w", encoding="utf-8") as output_file:
        json.dump(schema, output_file, ensure_ascii=False, indent=4)
schema_required = summarize_required(conversations) 
filename = "schema_anthropic_required.json"
filepath = os.path.join(f"_conversations_schema", filename)
with open(filepath, "w", encoding="utf-8") as output_file:
        json.dump(schema_required, output_file, ensure_ascii=False, indent=4)

# OPENAI ================
with open("_import_conversations🔒/_conversations_openai.json", "r", encoding="utf-8") as f:
        conversations = json.load(f)
schema = summarize(conversations)
del schema["!)mapping"]["?)placeholder-request-WEB:a85162a2-94ba-4cfe-bca5-77653adf0b37-1"]
filename = "schema_openai_full.json"
filepath = os.path.join(f"_conversations_schema", filename)
with open(filepath, "w", encoding="utf-8") as output_file:
        json.dump(schema, output_file, ensure_ascii=False, indent=4)
schema_required = summarize_required(conversations) 
filename = "schema_openai_required.json"
filepath = os.path.join(f"_conversations_schema", filename)
with open(filepath, "w", encoding="utf-8") as output_file:
        json.dump(schema_required, output_file, ensure_ascii=False, indent=4)

"""DOCS"""
"""
Generates a clean structural schema from a large JSON file.
Parses the entire dataset — no sampling.
Arrays are represented as dicts with "_maxlen": <count>.
Every key is prefixed with !) if required in all instances, ?) if optional.
Simple fields are output before nested objects/arrays.
"""