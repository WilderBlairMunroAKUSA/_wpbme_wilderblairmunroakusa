#!/usr/bin/env python3


#def valu

def universalize(data):
    """
    Transforms JSON data into a recursive ["type", [data]] stream.
    """
    if isinstance(data, dict):
        # We treat objects as a list of "key" typed pairs
		#members = []
#		for k, v in data.items():
#			element = ["element", universalize(v)]
#			member = ["member", 
#["member", [["string", [str(k)]], ["element", universalize(v)]]
        return ["value", ["object", [["member", [["name", ["string", [str(k)]]], ["element", universalize(v)]]] for k, v in data.items()]]]
    
    elif isinstance(data, list):
        return ["value", ["array", [["element", universalize(item)] for item in data]]]
    
    elif isinstance(data, str):
        return ["value", ["string", [data]]]
    
    elif isinstance(data, bool):
        return ["value", [f"{data}", [data]]]
    
    elif isinstance(data, (int, float)):
        return ["value", ["number", [data]]]
    
    elif data is None:
        return ["value", ["null", [None]]]
    
    return ["unknown", str(data)]

def reconstruct(u_data):
    """
    Rebuilds standard JSON-ready objects from the ["type", data] format.
    """
    u_type, payload = u_data

    if u_type == "object":
        # payload is a list of [key, [val_type, val_payload]]
        return {k: reconstruct(v) for k, v in payload}

    if u_type == "array":
        # payload is a list of ["type", payload]
        return [reconstruct(item) for item in payload]

    # Otherwise, it's a primitive (string, number, boolean, null)
    # The payload is already the literal value
    return payload

# Verification Loop:
# original -> universalize -> reconstruct -> compare
# processed = reconstruct(universal_tree)
# assert processed == json.loads(raw)


# Test Example
import json
import os

with open("130-wilderblairmunroakusa-claude-250924.json", "r", encoding="utf-8") as f:
        conversation = json.load(f)


filename = "_output.json"
filepath = os.path.join(f".", filename)
raw = """{
  "user": "dev",
  "tags": [
    "AI",
    "Sparse",
    [
      1,
      2,
      null,
	  -0
    ],
    {
      "key": {
        "sub1": "val1",
        "sub1": false
      }
    }
  ],
  "active": true,
  "key": {}
}"""

print(json.dumps(json.loads(raw), indent=2))
universal_tree = universalize(json.loads(raw))
print(json.dumps(universal_tree, indent=2))

#print(json.dumps(reconstruct(universal_tree), indent=2))


with open(filepath, "w", encoding="utf-8") as output_file:
        json.dump(universal_tree, output_file, ensure_ascii=False, indent=2)
