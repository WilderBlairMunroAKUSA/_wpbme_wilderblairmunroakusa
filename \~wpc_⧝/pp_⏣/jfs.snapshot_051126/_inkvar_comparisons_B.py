#!/usr/bin/env python3

""" unicode block python char definitions"""
"""control characters"""
CBL = 0x0000			# CBL := unicode control & basic latin block
C0_START = CBL + 0x0	# C0  := CBL contro character subblock
C0_END = 0x1F
C0_LEN = C0_END - C0_START + 1 # 32
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
U00XX, |U00X0, |U00X1, |U00X2, |  ⋯ <-16B-> ⋯  |U00XD, |U00XE, |U00XF, |
-------+-------|-------|-------|-------⋯-------|-------|-------|-------|
x000X  | ⋱
x001X  |
--------"""
\
\
C0NUL	\
	 ,	C0SOH,	C0STX,	C0ETX,	C0EOT	\
									 ,	C0ENQ,	C0ACK,	C0BEL,	\
C0BS_	\
	 ,	C0HT_,	C0LF_,	C0VT_,	C0FF_,	C0CR_	\
											 ,	C0SO_,	C0SI_,	\
\
CODLE	\
	 ,	C0DC1,	C0DC2,	C0DC3,	C0DC4	\
									 ,	C0NAK,	C0SYN,	C0ETB,	\
C0CAN	\
	 ,	C0EM_,	C0SUB,	C0ESC	\
							 ,	C0FS_,	C0GS_,	C0RS_,	C0US_	\
\
\
=\
tuple(chr(C0_START + i) for i in range(C0_LEN))
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


PC_START = CBL + 0x20	# PC := CBL basic latin character subblock
PC_END = 0x7E
PC_LEN = PC_END - PC_START + 1 # 95
""" CBL basic latin subblock definition: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
U00XX, |U00X0, |U00X1, |U00X2, |  ⋯ <-16B-> ⋯  |U00XD, |U00XE, |U00XF, |
-------+-------|-------|-------|-------⋯-------|-------|-------|-------|
x002X  | ⋱
x003X  |
⋮  ⋮   ⋮
x006X  |
x007X  |
--------"""
\
\
\
PCSPC	\
	 ,	PCBNG,	PCDQ_,	PCHSH,	PCDOL,	PCPRC,	PCAMP,	PCSQ_,	\
PCPR_,	PC_PR	\
			 ,	PCAST,	PCPLS,	PCCOM,	PCMIN,	PCDOT,	PCFSL,	\
\
PC_0_	\
	 ,	PC_1_,	PC_2_,	PC_3_,	PC_4_,	PC_5_,	PC_6_,	PC_7_,	\
PC_8_,	PC_9_	\
			 ,	PCCOL,	PCSMC	\
							 ,	PCLT_,	PCEQL,	PC_GT	\
													 ,	PCQUE,	\
\
\
PC_AT	\
	 ,	PC_A_,	PC_B_,	PC_C_,	PC_D_,	PC_E_,	PC_F_,	PC_G_,	\
PC_H_,	PC_I_,	PC_J_,	PC_K_,	PC_L_,	PC_M_,	PC_N_,	PC_O_,	\
\
PC_P_,	PC_Q_,	PC_R_,	PC_S_,	PC_T_,	PC_U_,	PC_V_,	PC_W_,	\
PC_X_,	PC_Y_,	PC_Z_	\
					 ,	PCSB_,	PCBSL,	PC_SB	\
											 ,	PCCFX,	PCUND,	\
\
\
PCBAC	\
	 ,	PC_a_,	PC_b_,	PC_c_,	PC_d_,	PC_e_,	PC_f_,	PC_g_,	\
PC_h_,	PC_i_,	PC_j_,	PC_k_,	PC_l_,	PC_m_,	PC_n_,	PC_o_,	\
\
PC_p_,	PC_q_,	PC_r_,	PC_s_,	PC_t_,	PC_u_,	PC_v_,	PC_w_,	\
PC_x_,	PC_y_,	PC_z_	\
					 ,	PCCB_,	PCVBR,	PC_CB	\
											 ,	PCTLD	\
\
\
													 ,	__DEL	\
\
=\
tuple(chr(PC_START + i) for i in range(PC_LEN + 1)) # include DEL
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


"""define: b256 dense byte encoding 1-channel block"""
VS0 = 0xFE00 # VS = variation selector block
VS0_START = 0xFE00
VS0_END = 0xFE0F
VS0_LEN = VS0_END - VS0_START + 1 # 16
VSS = 0xE0100 # VSS = variation selector supplementary block
VSS_START = 0xE0100
VSS_END = 0xE01EF
VSS_LEN = VSS_END - VSS_START + 1 # 240
"""..........................................................."""
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
VSxXX, |U00X0, |U00X1, |U00X2, |  ⋯ <-16B-> ⋯  |U00XD, |U00XE, |U00XF, |
|------+-------|-------|-------|--⋯----⋯-------|-------|-------|-------|
|x002X | ⋱
|x003X |
⋮  ⋮   ⋮
|x006X |
|x007X |
-----"""

VSx00	\
	 ,	VSx01,	VSx02,	VSx03,	VSx04,	VSx05,	VSx06,	VSx07,	\
VSx08,	VSx09,	VSx0A,	VSx0B,	VSx0C,	VSx0D,	VSx0E	\
													 ,	VSx0F,	\
\
VSx10	\
	,	VSx11,	VSx12,	VSx13,	VSx14,	VSx15,	VSx16,	VSx17,	\
VSx18,	VSx19,	VSx1A,	VSx1B,	VSx1C,	VSx1D,	VSx1E,	VSx1F,	\
\
VSx20,	VSx21,	VSx22,	VSx23,	VSx24,	VSx25,	VSx26,	VSx27,	\
VSx28,	VSx29,	VSx2A,	VSx2B,	VSx2C,	VSx2D,	VSx2E,	VSx2F,	\
\
VSx30,	VSx31,	VSx32,	VSx33,	VSx34,	VSx35,	VSx36,	VSx37,	\
VSx38,	VSx39,	VSx3A,	VSx3B,	VSx3C,	VSx3D,	VSx3E,	VSx3F,	\
\
VSx40,	VSx41,	VSx42,	VSx43,	VSx44,	VSx45,	VSx46,	VSx47,	\
VSx48,	VSx49,	VSx4A,	VSx4B,	VSx4C,	VSx4D,	VSx4E,	VSx4F,	\
\
VSx50,	VSx51,	VSx52,	VSx53,	VSx54,	VSx55,	VSx56,	VSx57,	\
VSx58,	VSx59,	VSx5A,	VSx5B,	VSx5C,	VSx5D,	VSx5E,	VSx5F,	\
\
VSx60,	VSx61,	VSx62,	VSx63,	VSx64,	VSx65,	VSx66,	VSx67,	\
VSx68,	VSx69,	VSx6A,	VSx6B,	VSx6C,	VSx6D,	VSx6E,	VSx6F,	\
\
VSx70,	VSx71,	VSx72,	VSx73,	VSx74,	VSx75,	VSx76,	VSx77,	\
VSx78,	VSx79,	VSx7A,	VSx7B,	VSx7C,	VSx7D,	VSx7E,	VSx7F,	\
\
VSx80,	VSx81,	VSx82,	VSx83,	VSx84,	VSx85,	VSx86,	VSx87,	\
VSx88,	VSx89,	VSx8A,	VSx8B,	VSx8C,	VSx8D,	VSx8E,	VSx8F,	\
\
VSx90,	VSx91,	VSx92,	VSx93,	VSx94,	VSx95,	VSx96,	VSx97,	\
VSx98,	VSx99,	VSx9A,	VSx9B,	VSx9C,	VSx9D,	VSx9E,	VSx9F,	\
\
VSxA0,	VSxA1,	VSxA2,	VSxA3,	VSxA4,	VSxA5,	VSxA6,	VSxA7,	\
VSxA8,	VSxA9,	VSxAA,	VSxAB,	VSxAC,	VSxAD,	VSxAE,	VSxAF,	\
\
VSxB0,	VSxB1,	VSxB2,	VSxB3,	VSxB4,	VSxB5,	VSxB6,	VSxB7,	\
VSxB8,	VSxB9,	VSxBA,	VSxBB,	VSxBC,	VSxBD,	VSxBE,	VSxBF,	\
\
VSxC0,	VSxC1,	VSxC2,	VSxC3,	VSxC4,	VSxC5,	VSxC6,	VSxC7,	\
VSxC8,	VSxC9,	VSxCA,	VSxCB,	VSxCC,	VSxCD,	VSxCE,	VSxCF,	\
\
VSxD0,	VSxD1,	VSxD2,	VSxD3,	VSxD4,	VSxD5,	VSxD6,	VSxD7,	\
VSxD8,	VSxD9,	VSxDA,	VSxDB,	VSxDC,	VSxDD,	VSxDE,	VSxDF,	\
\
VSxE0,	VSxE1,	VSxE2,	VSxE3,	VSxE4,	VSxE5,	VSxE6,	VSxE7,	\
VSxE8,	VSxE9,	VSxEA,	VSxEB,	VSxEC,	VSxED,	VSxEE,	VSxEF,	\
\
VSxF0,	VSxF1,	VSxF2,	VSxF3,	VSxF4,	VSxF5,	VSxF6,	VSxF7,	\
VSxF8,	VSxF9,	VSxFA,	VSxFB,	VSxFC,	VSxFD,	VSxFE	\
\
													 ,	VSxFF	\
\
\
= \
tuple(chr(VS0_START + i) for i in range(VS0_LEN)) + \
tuple(chr(VSS_START + i) for i in range(VSS_LEN))
"""..........................................................."""

# VS = {
#	 f"{i:03d}": chr(VS0_START + i)
#	 if i <= VS0_END
#	 else chr(VSS_START + i)
#	 for i in range(VS0_LEN + VSS_LEN)}

# """define: tags"""
# TAG = 0xE0000 # TG = tags block

# TAG_START = TAG + PC_START
# TAG_END = TAG + PC_END + 1
# TAG_LEN = TAG_END - TAG_START


# TAG_BEGIN = 0xE0001

# # TG = {
# #	 f"{i:03d}": chr(TAG_START + i)
# #	 if i <= TAG_END
# #	 else chr(VSS_START + i)
# #	 for i in range(VS0_LEN + VSS_LEN)}


# TGx20,	TGx21,	TGx22,	TGx23,	TGx24,	TGx25,	TGx26,	TGx27,	\
# TGx28,	TGx29,	TGx2A,	TGx2B,	TGx2C,	TGx2D,	TGx2E,	TGx2F,	\
# TGx30,	TGx31,	TGx32,	TGx33,	TGx34,	TGx35,	TGx36,	TGx37,	\
# TGx38,	TGx39,	TGx3A,	TGx3B,	TGx3C,	TGx3D,	TGx3E,	TGx3F,	\
# TGx40,	TGx41,	TGx42,	TGx43,	TGx44,	TGx45,	TGx46,	TGx47,	\
# TGx48,	TGx49,	TGx4A,	TGx4B,	TGx4C,	TGx4D,	TGx4E,	TGx4F,	\
# TGx50,	TGx51,	TGx52,	TGx53,	TGx54,	TGx55,	TGx56,	TGx57,	\
# TGx58,	TGx59,	TGx5A,	TGx5B,	TGx5C,	TGx5D,	TGx5E,	TGx5F,	\
# TGx60,	TGx61,	TGx62,	TGx63,	TGx64,	TGx65,	TGx66,	TGx67,	\
# TGx68,	TGx69,	TGx6A,	TGx6B,	TGx6C,	TGx6D,	TGx6E,	TGx6F,	\
# TGx70,	TGx71,	TGx72,	TGx73,	TGx74,	TGx75,	TGx76,	TGx77,	\
# TGx78,	TGx79,	TGx7A,	TGx7B,	TGx7C,	TGx7D,	TGx7E			\
#													,	TGx7F	\
# = \
# (None, TAG_BEGIN) + \
# tuple(None for i in range(C0_LEN - 2)) + \
# tuple(chr(TG + i) for i in range(TAG_LEN - C0_LEN))

