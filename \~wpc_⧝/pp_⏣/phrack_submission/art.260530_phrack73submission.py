#![no_std]														#
#64B/lord														#
#This is a valid utf-8 encoded md file.							#
#This is a submission to Phrack 73.								#
#Author: WilderBlairMunroAKUSA									#
VS, VS_START, VS_END		= 0xFE00, 0xFE00, 0xFE0F			#
VSP, VSP_START, VSP_END		= 0xE0100, 0xE0100, 0xE01EF			#
def vsiink_to_utf8(vsiink_str):									#
	Bs = []														#
	for ch in vsiink_str:										#
		if VS_START <= ord(ch) <= VS_END:						#
			Bs.append(ord(ch) - VS_START)						#
		elif VSP_START <= ord(ch) <= VSP_END:					#
			Bs.append((ord(ch) - VSP_START) + 16)				#
	return bytes(Bs).decode('utf-8')							#


