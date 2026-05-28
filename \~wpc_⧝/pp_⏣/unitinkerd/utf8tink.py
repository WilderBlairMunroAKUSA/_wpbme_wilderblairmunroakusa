#!/usr/bin/env python3

#for x in range(0xFE00, 0xFE0F):
	#print(chr(0xE0100 + x).encode('utf-8'))
	#print(chr(x).encode('utf-8'))
print(chr(0xE0161).encode('utf-8'))





"""octal tinker"""

mits
(0) <-> (0) <-> (1) ~ mX

bits
(0)(1) <-> (0)(1) <-> (1)(2)~ bX

niblets
(00)(01)(10)(11) <-> (0)(1)(2)(3) <-> (1)(2)(3)(4) ~ nX

triblets
(000)(001)...(110)(111) <-> (0)(1)...(6)(7) <-> (1)(2)...(7)(8)~ oX

nibbles (hex)
(0000)...(1111) <-> (0)...(15) <-> (1)(2)...(15)(16) 
...

\n2\n1\n0 ~ \n2(\n10) ~ \n\h == octal double word 2^6 = 64

bit trit
(1)(1)(1) ==~ (0)(1)(2)==(b)(bb) ~ (b)(n) = (b1)(11) = (b1)(n3) [2^1][2^2]
2^3


mit trit
(0)(0)(0) == (m0)(m00) = (m0)(b1) (0)(1) == [2^0][2^1] {(m_)(b0)[0], (m0)(b0)[1], (m0)(b1)[2]} ==> m00=d1, m0=d0
mitlet
(mm) in (0, 1), mitlet double = mit trit

bit trit, only symbols 0 and 1 {m0=0, m00=1} (base 2) {symbol*1 + 1}
(b)(b)(b) == (b)(bb) == (b)((mm)(mm)) = (b)((m(b))(m(b))) + 2 and 3


bit trit, bit niblet, only symbols 0,1,2,3 (base 4 ->8) symbols*2+1
(b)(n) == (b)(n) == (b)(n) -> octit

1-7 * 2 plus 1 hex

...

(b)(o)(o) == (o)(h) [128, 2^7]=[2^1][2^6] or [2^1][64]

....
(?)(h)(h) ! not pattern, bad attempt

!
hex trit
(h)(h)(h) ==  == (h)(B) == (o)(ooo) [2^3][2^9]

-!-
(n)(n)(n) = (n)(h) = (o)(o) = [2^3][2^3] = [64]

(b)(o) = [16] , (b)(h) = [32] = (n)(o)

(b)(b) = [4]	(b)(n) = [8]
(n)(n) = [16]	(n)(o) = [32] = (b)(h)
(o)(o) = [64]	(o)(h) = [128]
(h)(h) = [256]

(o)(o) ==~ niblet is to octal double like octal double is to niblit trit to niblet hex

(oo)(oo)(oo) == (oo)(h)(B) = (h)[(o)(h) (o)(h)] = (n)(h)(n)(h)(n)(h)
												=(b)(h) (b)(h) (b)(h) (b)(h)


2^5 = 32 ... 3* 2^5 = 96
b*h:32 :: h*256 [4^1* 4^4]

b(ooo) -> 128 from 64
? asci like (o)->(h)
so, hex from o double word 3  niblet trit like oo nnn nh
Byte from nib trip / odouble double or hex quad (256)
like !!! o:h::((nh)(nh)==hhh)

vis asci: like no: oh::nn :oo
