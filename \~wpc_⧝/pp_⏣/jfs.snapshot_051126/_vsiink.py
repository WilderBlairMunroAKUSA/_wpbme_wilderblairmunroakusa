#!/usr/bin/env python3
"""DOCS:
(*written in variation selector invisible ink)

"""
import typing
import binascii
from _inkvar import *



class Channel1Overwrite(ValueError):
    pass

def _vsiink_from_uuid(uuid_str: str) -> str:
    """conceal: cast ascii text uuid as base-256 vsiink"""
    cleaned = ''.join(c for c in uuid_str if c in '0123456789abcdefABCDEF')
    raw_bytes = binascii.unhexlify(cleaned)
    vsiink = []
    for b in raw_bytes:
        if b <= 0x0F: vsiink.append(chr(0xFE00 + b)) # VS1–VS16
        else: vsiink.append(chr(0xE0100 + (b - 0x10))) # VS17–VS256
    return "".join(vsiink)

def _vsiink_to_uuid(text: str) -> str:
    """reveal: cast vsiink base-256 uuid as ascii text"""
    raw_bytes = []
    for char in text:
        cp = ord(char)
        if 0xFE00 <= cp <= 0xFE0F: # VS1-16
            raw_bytes.append(cp - 0xFE00)
        elif 0xE0100 <= cp <= 0xE01EF: # VS17-256
            raw_bytes.append((cp - 0xE0100) + 0x10)
    if not raw_bytes: return ""
    hex_str = binascii.hexlify(bytes(raw_bytes)).decode('ascii')
    if len(hex_str) == 32:
        return f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"
    return hex_str

def _vsiink_from_ascii(text: str,
    mode: typing.Literal["DENSE", "CHUNK", "SAFE"]="DENSE") -> str:
    """conceal: cast ascii text to vsink ascii"""
    vsiink = []
    channel_1_active = False
    for char in text:
        cp = ord(char)
        if cp in (0x7F, 0xE016F, 0xE01EF): continue # delete chars
            # (3-bit delete char bracket logic hook)
        if 0xE0170 <= cp <= 0xE01EE:
                channel_1_active = True
        # if control / visible ascii, map to channel block 0, VS1-127
        if cp <= 0x0F: vsiink.append(chr(0xFE00 + b)) # VS1–VS16
        elif cp <= 0xFE: vsiink.append(chr(0xE0100 + cp)) # VS17-127
        # map entire channel block 0 to channel block 1, VS129-255
        elif 0xE0100 <= cp <= 0xE016E:
            # if ascii vsiink not already occupying channel block 1,
            if channel_1_active: raise Channel1Overwrite()
            vsiink.append(chr(cp + 128))
        else: continue
        if mode == "DENSE": continue
    return "".join(vsiink)

# ==================== Main Test ====================

test_uuid = "01020304-0506-0708-090a-0b0c0d0e0f10"
test_ascii_pure = ""
test_ascii_mixed = ""

print('"testkey": "testvalue"')

for n in range(5):
    print(".", end="")                                 # visible separator
    stealth = _vsiink_from_uuid(test_uuid)
    #sys.stdout.buffer.write(stealth.encode('utf-8'))   # CRITICAL: raw bytes
    print("" + stealth + "", end="")
    print(f".{C0NUL}", end="")                                 # visible separator

print()  # newline
print('"testkey": "testvalue"')
#print("ping")

