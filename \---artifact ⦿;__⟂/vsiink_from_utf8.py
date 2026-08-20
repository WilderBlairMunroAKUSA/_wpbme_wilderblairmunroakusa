#!/usr/bin/env python3
import sys
DEL								= 0x7F
NUL_STR							= ''
VS,  VS_START,  VS_END			= 0xFE00,  0xFE00,  0xFE0F
VSP, VSP_START, VSP_END			= 0xE0100, 0xE0100, 0xE01EF
# turning off DEL pad for now
def vsiink_from_utf8(utf8_str):
# vsiink	:= variation selector invisible ink
# Bs		:= Bytes
	Bs = utf8_str.encode('utf-8')
	vsiink = []
	for b in Bs:
		#if b < 16: vsiink.append(chr(DEL) + chr(VS_START + b))	# VS1–VS16
		if b < 16: vsiink.append(chr(VS_START + b))	# VS1–VS16
		else: vsiink.append(chr(VSP_START + (b - 16)))			# VS17–VS256
	return NUL_STR.join(vsiink)
if __name__ == "__main__":
    print(f'"{vsiink_from_utf8(sys.argv[1])}"')
