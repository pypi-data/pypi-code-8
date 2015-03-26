# This file is part of 'NTLM Authorization Proxy Server'
# Copyright 2001 Dmitry A. Rozmanov <dima@xenon.spb.ru>
#
# NTLM APS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# NTLM APS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the sofware; see the file COPYING. If not, write to the
# Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#

from U32 import U32

# static unsigned long des_SPtrans[8][64]={

des_SPtrans =\
[
#nibble 0
[
U32(0x00820200L), U32(0x00020000L), U32(0x80800000L), U32(0x80820200L),
U32(0x00800000L), U32(0x80020200L), U32(0x80020000L), U32(0x80800000L),
U32(0x80020200L), U32(0x00820200L), U32(0x00820000L), U32(0x80000200L),
U32(0x80800200L), U32(0x00800000L), U32(0x00000000L), U32(0x80020000L),
U32(0x00020000L), U32(0x80000000L), U32(0x00800200L), U32(0x00020200L),
U32(0x80820200L), U32(0x00820000L), U32(0x80000200L), U32(0x00800200L),
U32(0x80000000L), U32(0x00000200L), U32(0x00020200L), U32(0x80820000L),
U32(0x00000200L), U32(0x80800200L), U32(0x80820000L), U32(0x00000000L),
U32(0x00000000L), U32(0x80820200L), U32(0x00800200L), U32(0x80020000L),
U32(0x00820200L), U32(0x00020000L), U32(0x80000200L), U32(0x00800200L),
U32(0x80820000L), U32(0x00000200L), U32(0x00020200L), U32(0x80800000L),
U32(0x80020200L), U32(0x80000000L), U32(0x80800000L), U32(0x00820000L),
U32(0x80820200L), U32(0x00020200L), U32(0x00820000L), U32(0x80800200L),
U32(0x00800000L), U32(0x80000200L), U32(0x80020000L), U32(0x00000000L),
U32(0x00020000L), U32(0x00800000L), U32(0x80800200L), U32(0x00820200L),
U32(0x80000000L), U32(0x80820000L), U32(0x00000200L), U32(0x80020200L),
],

#nibble 1
[
U32(0x10042004L), U32(0x00000000L), U32(0x00042000L), U32(0x10040000L),
U32(0x10000004L), U32(0x00002004L), U32(0x10002000L), U32(0x00042000L),
U32(0x00002000L), U32(0x10040004L), U32(0x00000004L), U32(0x10002000L),
U32(0x00040004L), U32(0x10042000L), U32(0x10040000L), U32(0x00000004L),
U32(0x00040000L), U32(0x10002004L), U32(0x10040004L), U32(0x00002000L),
U32(0x00042004L), U32(0x10000000L), U32(0x00000000L), U32(0x00040004L),
U32(0x10002004L), U32(0x00042004L), U32(0x10042000L), U32(0x10000004L),
U32(0x10000000L), U32(0x00040000L), U32(0x00002004L), U32(0x10042004L),
U32(0x00040004L), U32(0x10042000L), U32(0x10002000L), U32(0x00042004L),
U32(0x10042004L), U32(0x00040004L), U32(0x10000004L), U32(0x00000000L),
U32(0x10000000L), U32(0x00002004L), U32(0x00040000L), U32(0x10040004L),
U32(0x00002000L), U32(0x10000000L), U32(0x00042004L), U32(0x10002004L),
U32(0x10042000L), U32(0x00002000L), U32(0x00000000L), U32(0x10000004L),
U32(0x00000004L), U32(0x10042004L), U32(0x00042000L), U32(0x10040000L),
U32(0x10040004L), U32(0x00040000L), U32(0x00002004L), U32(0x10002000L),
U32(0x10002004L), U32(0x00000004L), U32(0x10040000L), U32(0x00042000L),
],

#nibble 2
[
U32(0x41000000L), U32(0x01010040L), U32(0x00000040L), U32(0x41000040L),
U32(0x40010000L), U32(0x01000000L), U32(0x41000040L), U32(0x00010040L),
U32(0x01000040L), U32(0x00010000L), U32(0x01010000L), U32(0x40000000L),
U32(0x41010040L), U32(0x40000040L), U32(0x40000000L), U32(0x41010000L),
U32(0x00000000L), U32(0x40010000L), U32(0x01010040L), U32(0x00000040L),
U32(0x40000040L), U32(0x41010040L), U32(0x00010000L), U32(0x41000000L),
U32(0x41010000L), U32(0x01000040L), U32(0x40010040L), U32(0x01010000L),
U32(0x00010040L), U32(0x00000000L), U32(0x01000000L), U32(0x40010040L),
U32(0x01010040L), U32(0x00000040L), U32(0x40000000L), U32(0x00010000L),
U32(0x40000040L), U32(0x40010000L), U32(0x01010000L), U32(0x41000040L),
U32(0x00000000L), U32(0x01010040L), U32(0x00010040L), U32(0x41010000L),
U32(0x40010000L), U32(0x01000000L), U32(0x41010040L), U32(0x40000000L),
U32(0x40010040L), U32(0x41000000L), U32(0x01000000L), U32(0x41010040L),
U32(0x00010000L), U32(0x01000040L), U32(0x41000040L), U32(0x00010040L),
U32(0x01000040L), U32(0x00000000L), U32(0x41010000L), U32(0x40000040L),
U32(0x41000000L), U32(0x40010040L), U32(0x00000040L), U32(0x01010000L),
],

#nibble 3
[
U32(0x00100402L), U32(0x04000400L), U32(0x00000002L), U32(0x04100402L),
U32(0x00000000L), U32(0x04100000L), U32(0x04000402L), U32(0x00100002L),
U32(0x04100400L), U32(0x04000002L), U32(0x04000000L), U32(0x00000402L),
U32(0x04000002L), U32(0x00100402L), U32(0x00100000L), U32(0x04000000L),
U32(0x04100002L), U32(0x00100400L), U32(0x00000400L), U32(0x00000002L),
U32(0x00100400L), U32(0x04000402L), U32(0x04100000L), U32(0x00000400L),
U32(0x00000402L), U32(0x00000000L), U32(0x00100002L), U32(0x04100400L),
U32(0x04000400L), U32(0x04100002L), U32(0x04100402L), U32(0x00100000L),
U32(0x04100002L), U32(0x00000402L), U32(0x00100000L), U32(0x04000002L),
U32(0x00100400L), U32(0x04000400L), U32(0x00000002L), U32(0x04100000L),
U32(0x04000402L), U32(0x00000000L), U32(0x00000400L), U32(0x00100002L),
U32(0x00000000L), U32(0x04100002L), U32(0x04100400L), U32(0x00000400L),
U32(0x04000000L), U32(0x04100402L), U32(0x00100402L), U32(0x00100000L),
U32(0x04100402L), U32(0x00000002L), U32(0x04000400L), U32(0x00100402L),
U32(0x00100002L), U32(0x00100400L), U32(0x04100000L), U32(0x04000402L),
U32(0x00000402L), U32(0x04000000L), U32(0x04000002L), U32(0x04100400L),
],

#nibble 4
[
U32(0x02000000L), U32(0x00004000L), U32(0x00000100L), U32(0x02004108L),
U32(0x02004008L), U32(0x02000100L), U32(0x00004108L), U32(0x02004000L),
U32(0x00004000L), U32(0x00000008L), U32(0x02000008L), U32(0x00004100L),
U32(0x02000108L), U32(0x02004008L), U32(0x02004100L), U32(0x00000000L),
U32(0x00004100L), U32(0x02000000L), U32(0x00004008L), U32(0x00000108L),
U32(0x02000100L), U32(0x00004108L), U32(0x00000000L), U32(0x02000008L),
U32(0x00000008L), U32(0x02000108L), U32(0x02004108L), U32(0x00004008L),
U32(0x02004000L), U32(0x00000100L), U32(0x00000108L), U32(0x02004100L),
U32(0x02004100L), U32(0x02000108L), U32(0x00004008L), U32(0x02004000L),
U32(0x00004000L), U32(0x00000008L), U32(0x02000008L), U32(0x02000100L),
U32(0x02000000L), U32(0x00004100L), U32(0x02004108L), U32(0x00000000L),
U32(0x00004108L), U32(0x02000000L), U32(0x00000100L), U32(0x00004008L),
U32(0x02000108L), U32(0x00000100L), U32(0x00000000L), U32(0x02004108L),
U32(0x02004008L), U32(0x02004100L), U32(0x00000108L), U32(0x00004000L),
U32(0x00004100L), U32(0x02004008L), U32(0x02000100L), U32(0x00000108L),
U32(0x00000008L), U32(0x00004108L), U32(0x02004000L), U32(0x02000008L),
],

#nibble 5
[
U32(0x20000010L), U32(0x00080010L), U32(0x00000000L), U32(0x20080800L),
U32(0x00080010L), U32(0x00000800L), U32(0x20000810L), U32(0x00080000L),
U32(0x00000810L), U32(0x20080810L), U32(0x00080800L), U32(0x20000000L),
U32(0x20000800L), U32(0x20000010L), U32(0x20080000L), U32(0x00080810L),
U32(0x00080000L), U32(0x20000810L), U32(0x20080010L), U32(0x00000000L),
U32(0x00000800L), U32(0x00000010L), U32(0x20080800L), U32(0x20080010L),
U32(0x20080810L), U32(0x20080000L), U32(0x20000000L), U32(0x00000810L),
U32(0x00000010L), U32(0x00080800L), U32(0x00080810L), U32(0x20000800L),
U32(0x00000810L), U32(0x20000000L), U32(0x20000800L), U32(0x00080810L),
U32(0x20080800L), U32(0x00080010L), U32(0x00000000L), U32(0x20000800L),
U32(0x20000000L), U32(0x00000800L), U32(0x20080010L), U32(0x00080000L),
U32(0x00080010L), U32(0x20080810L), U32(0x00080800L), U32(0x00000010L),
U32(0x20080810L), U32(0x00080800L), U32(0x00080000L), U32(0x20000810L),
U32(0x20000010L), U32(0x20080000L), U32(0x00080810L), U32(0x00000000L),
U32(0x00000800L), U32(0x20000010L), U32(0x20000810L), U32(0x20080800L),
U32(0x20080000L), U32(0x00000810L), U32(0x00000010L), U32(0x20080010L),
],

#nibble 6
[
U32(0x00001000L), U32(0x00000080L), U32(0x00400080L), U32(0x00400001L),
U32(0x00401081L), U32(0x00001001L), U32(0x00001080L), U32(0x00000000L),
U32(0x00400000L), U32(0x00400081L), U32(0x00000081L), U32(0x00401000L),
U32(0x00000001L), U32(0x00401080L), U32(0x00401000L), U32(0x00000081L),
U32(0x00400081L), U32(0x00001000L), U32(0x00001001L), U32(0x00401081L),
U32(0x00000000L), U32(0x00400080L), U32(0x00400001L), U32(0x00001080L),
U32(0x00401001L), U32(0x00001081L), U32(0x00401080L), U32(0x00000001L),
U32(0x00001081L), U32(0x00401001L), U32(0x00000080L), U32(0x00400000L),
U32(0x00001081L), U32(0x00401000L), U32(0x00401001L), U32(0x00000081L),
U32(0x00001000L), U32(0x00000080L), U32(0x00400000L), U32(0x00401001L),
U32(0x00400081L), U32(0x00001081L), U32(0x00001080L), U32(0x00000000L),
U32(0x00000080L), U32(0x00400001L), U32(0x00000001L), U32(0x00400080L),
U32(0x00000000L), U32(0x00400081L), U32(0x00400080L), U32(0x00001080L),
U32(0x00000081L), U32(0x00001000L), U32(0x00401081L), U32(0x00400000L),
U32(0x00401080L), U32(0x00000001L), U32(0x00001001L), U32(0x00401081L),
U32(0x00400001L), U32(0x00401080L), U32(0x00401000L), U32(0x00001001L),
],

#nibble 7
[
U32(0x08200020L), U32(0x08208000L), U32(0x00008020L), U32(0x00000000L),
U32(0x08008000L), U32(0x00200020L), U32(0x08200000L), U32(0x08208020L),
U32(0x00000020L), U32(0x08000000L), U32(0x00208000L), U32(0x00008020L),
U32(0x00208020L), U32(0x08008020L), U32(0x08000020L), U32(0x08200000L),
U32(0x00008000L), U32(0x00208020L), U32(0x00200020L), U32(0x08008000L),
U32(0x08208020L), U32(0x08000020L), U32(0x00000000L), U32(0x00208000L),
U32(0x08000000L), U32(0x00200000L), U32(0x08008020L), U32(0x08200020L),
U32(0x00200000L), U32(0x00008000L), U32(0x08208000L), U32(0x00000020L),
U32(0x00200000L), U32(0x00008000L), U32(0x08000020L), U32(0x08208020L),
U32(0x00008020L), U32(0x08000000L), U32(0x00000000L), U32(0x00208000L),
U32(0x08200020L), U32(0x08008020L), U32(0x08008000L), U32(0x00200020L),
U32(0x08208000L), U32(0x00000020L), U32(0x00200020L), U32(0x08008000L),
U32(0x08208020L), U32(0x00200000L), U32(0x08200000L), U32(0x08000020L),
U32(0x00208000L), U32(0x00008020L), U32(0x08008020L), U32(0x08200000L),
U32(0x00000020L), U32(0x08208000L), U32(0x00208020L), U32(0x00000000L),
U32(0x08000000L), U32(0x08200020L), U32(0x00008000L), U32(0x00208020L),
],
]

#static unsigned long des_skb[8][64]={

des_skb = \
[
#for C bits (numbered as per FIPS 46) 1 2 3 4 5 6
[
U32(0x00000000L),U32(0x00000010L),U32(0x20000000L),U32(0x20000010L),
U32(0x00010000L),U32(0x00010010L),U32(0x20010000L),U32(0x20010010L),
U32(0x00000800L),U32(0x00000810L),U32(0x20000800L),U32(0x20000810L),
U32(0x00010800L),U32(0x00010810L),U32(0x20010800L),U32(0x20010810L),
U32(0x00000020L),U32(0x00000030L),U32(0x20000020L),U32(0x20000030L),
U32(0x00010020L),U32(0x00010030L),U32(0x20010020L),U32(0x20010030L),
U32(0x00000820L),U32(0x00000830L),U32(0x20000820L),U32(0x20000830L),
U32(0x00010820L),U32(0x00010830L),U32(0x20010820L),U32(0x20010830L),
U32(0x00080000L),U32(0x00080010L),U32(0x20080000L),U32(0x20080010L),
U32(0x00090000L),U32(0x00090010L),U32(0x20090000L),U32(0x20090010L),
U32(0x00080800L),U32(0x00080810L),U32(0x20080800L),U32(0x20080810L),
U32(0x00090800L),U32(0x00090810L),U32(0x20090800L),U32(0x20090810L),
U32(0x00080020L),U32(0x00080030L),U32(0x20080020L),U32(0x20080030L),
U32(0x00090020L),U32(0x00090030L),U32(0x20090020L),U32(0x20090030L),
U32(0x00080820L),U32(0x00080830L),U32(0x20080820L),U32(0x20080830L),
U32(0x00090820L),U32(0x00090830L),U32(0x20090820L),U32(0x20090830L),
],

#for C bits (numbered as per FIPS 46) 7 8 10 11 12 13
[
U32(0x00000000L),U32(0x02000000L),U32(0x00002000L),U32(0x02002000L),
U32(0x00200000L),U32(0x02200000L),U32(0x00202000L),U32(0x02202000L),
U32(0x00000004L),U32(0x02000004L),U32(0x00002004L),U32(0x02002004L),
U32(0x00200004L),U32(0x02200004L),U32(0x00202004L),U32(0x02202004L),
U32(0x00000400L),U32(0x02000400L),U32(0x00002400L),U32(0x02002400L),
U32(0x00200400L),U32(0x02200400L),U32(0x00202400L),U32(0x02202400L),
U32(0x00000404L),U32(0x02000404L),U32(0x00002404L),U32(0x02002404L),
U32(0x00200404L),U32(0x02200404L),U32(0x00202404L),U32(0x02202404L),
U32(0x10000000L),U32(0x12000000L),U32(0x10002000L),U32(0x12002000L),
U32(0x10200000L),U32(0x12200000L),U32(0x10202000L),U32(0x12202000L),
U32(0x10000004L),U32(0x12000004L),U32(0x10002004L),U32(0x12002004L),
U32(0x10200004L),U32(0x12200004L),U32(0x10202004L),U32(0x12202004L),
U32(0x10000400L),U32(0x12000400L),U32(0x10002400L),U32(0x12002400L),
U32(0x10200400L),U32(0x12200400L),U32(0x10202400L),U32(0x12202400L),
U32(0x10000404L),U32(0x12000404L),U32(0x10002404L),U32(0x12002404L),
U32(0x10200404L),U32(0x12200404L),U32(0x10202404L),U32(0x12202404L),
],

#for C bits (numbered as per FIPS 46) 14 15 16 17 19 20
[
U32(0x00000000L),U32(0x00000001L),U32(0x00040000L),U32(0x00040001L),
U32(0x01000000L),U32(0x01000001L),U32(0x01040000L),U32(0x01040001L),
U32(0x00000002L),U32(0x00000003L),U32(0x00040002L),U32(0x00040003L),
U32(0x01000002L),U32(0x01000003L),U32(0x01040002L),U32(0x01040003L),
U32(0x00000200L),U32(0x00000201L),U32(0x00040200L),U32(0x00040201L),
U32(0x01000200L),U32(0x01000201L),U32(0x01040200L),U32(0x01040201L),
U32(0x00000202L),U32(0x00000203L),U32(0x00040202L),U32(0x00040203L),
U32(0x01000202L),U32(0x01000203L),U32(0x01040202L),U32(0x01040203L),
U32(0x08000000L),U32(0x08000001L),U32(0x08040000L),U32(0x08040001L),
U32(0x09000000L),U32(0x09000001L),U32(0x09040000L),U32(0x09040001L),
U32(0x08000002L),U32(0x08000003L),U32(0x08040002L),U32(0x08040003L),
U32(0x09000002L),U32(0x09000003L),U32(0x09040002L),U32(0x09040003L),
U32(0x08000200L),U32(0x08000201L),U32(0x08040200L),U32(0x08040201L),
U32(0x09000200L),U32(0x09000201L),U32(0x09040200L),U32(0x09040201L),
U32(0x08000202L),U32(0x08000203L),U32(0x08040202L),U32(0x08040203L),
U32(0x09000202L),U32(0x09000203L),U32(0x09040202L),U32(0x09040203L),
],

#for C bits (numbered as per FIPS 46) 21 23 24 26 27 28
[
U32(0x00000000L),U32(0x00100000L),U32(0x00000100L),U32(0x00100100L),
U32(0x00000008L),U32(0x00100008L),U32(0x00000108L),U32(0x00100108L),
U32(0x00001000L),U32(0x00101000L),U32(0x00001100L),U32(0x00101100L),
U32(0x00001008L),U32(0x00101008L),U32(0x00001108L),U32(0x00101108L),
U32(0x04000000L),U32(0x04100000L),U32(0x04000100L),U32(0x04100100L),
U32(0x04000008L),U32(0x04100008L),U32(0x04000108L),U32(0x04100108L),
U32(0x04001000L),U32(0x04101000L),U32(0x04001100L),U32(0x04101100L),
U32(0x04001008L),U32(0x04101008L),U32(0x04001108L),U32(0x04101108L),
U32(0x00020000L),U32(0x00120000L),U32(0x00020100L),U32(0x00120100L),
U32(0x00020008L),U32(0x00120008L),U32(0x00020108L),U32(0x00120108L),
U32(0x00021000L),U32(0x00121000L),U32(0x00021100L),U32(0x00121100L),
U32(0x00021008L),U32(0x00121008L),U32(0x00021108L),U32(0x00121108L),
U32(0x04020000L),U32(0x04120000L),U32(0x04020100L),U32(0x04120100L),
U32(0x04020008L),U32(0x04120008L),U32(0x04020108L),U32(0x04120108L),
U32(0x04021000L),U32(0x04121000L),U32(0x04021100L),U32(0x04121100L),
U32(0x04021008L),U32(0x04121008L),U32(0x04021108L),U32(0x04121108L),
],

#for D bits (numbered as per FIPS 46) 1 2 3 4 5 6
[
U32(0x00000000L),U32(0x10000000L),U32(0x00010000L),U32(0x10010000L),
U32(0x00000004L),U32(0x10000004L),U32(0x00010004L),U32(0x10010004L),
U32(0x20000000L),U32(0x30000000L),U32(0x20010000L),U32(0x30010000L),
U32(0x20000004L),U32(0x30000004L),U32(0x20010004L),U32(0x30010004L),
U32(0x00100000L),U32(0x10100000L),U32(0x00110000L),U32(0x10110000L),
U32(0x00100004L),U32(0x10100004L),U32(0x00110004L),U32(0x10110004L),
U32(0x20100000L),U32(0x30100000L),U32(0x20110000L),U32(0x30110000L),
U32(0x20100004L),U32(0x30100004L),U32(0x20110004L),U32(0x30110004L),
U32(0x00001000L),U32(0x10001000L),U32(0x00011000L),U32(0x10011000L),
U32(0x00001004L),U32(0x10001004L),U32(0x00011004L),U32(0x10011004L),
U32(0x20001000L),U32(0x30001000L),U32(0x20011000L),U32(0x30011000L),
U32(0x20001004L),U32(0x30001004L),U32(0x20011004L),U32(0x30011004L),
U32(0x00101000L),U32(0x10101000L),U32(0x00111000L),U32(0x10111000L),
U32(0x00101004L),U32(0x10101004L),U32(0x00111004L),U32(0x10111004L),
U32(0x20101000L),U32(0x30101000L),U32(0x20111000L),U32(0x30111000L),
U32(0x20101004L),U32(0x30101004L),U32(0x20111004L),U32(0x30111004L),
],

#for D bits (numbered as per FIPS 46) 8 9 11 12 13 14
[
U32(0x00000000L),U32(0x08000000L),U32(0x00000008L),U32(0x08000008L),
U32(0x00000400L),U32(0x08000400L),U32(0x00000408L),U32(0x08000408L),
U32(0x00020000L),U32(0x08020000L),U32(0x00020008L),U32(0x08020008L),
U32(0x00020400L),U32(0x08020400L),U32(0x00020408L),U32(0x08020408L),
U32(0x00000001L),U32(0x08000001L),U32(0x00000009L),U32(0x08000009L),
U32(0x00000401L),U32(0x08000401L),U32(0x00000409L),U32(0x08000409L),
U32(0x00020001L),U32(0x08020001L),U32(0x00020009L),U32(0x08020009L),
U32(0x00020401L),U32(0x08020401L),U32(0x00020409L),U32(0x08020409L),
U32(0x02000000L),U32(0x0A000000L),U32(0x02000008L),U32(0x0A000008L),
U32(0x02000400L),U32(0x0A000400L),U32(0x02000408L),U32(0x0A000408L),
U32(0x02020000L),U32(0x0A020000L),U32(0x02020008L),U32(0x0A020008L),
U32(0x02020400L),U32(0x0A020400L),U32(0x02020408L),U32(0x0A020408L),
U32(0x02000001L),U32(0x0A000001L),U32(0x02000009L),U32(0x0A000009L),
U32(0x02000401L),U32(0x0A000401L),U32(0x02000409L),U32(0x0A000409L),
U32(0x02020001L),U32(0x0A020001L),U32(0x02020009L),U32(0x0A020009L),
U32(0x02020401L),U32(0x0A020401L),U32(0x02020409L),U32(0x0A020409L),
],

#for D bits (numbered as per FIPS 46) 16 17 18 19 20 21
[
U32(0x00000000L),U32(0x00000100L),U32(0x00080000L),U32(0x00080100L),
U32(0x01000000L),U32(0x01000100L),U32(0x01080000L),U32(0x01080100L),
U32(0x00000010L),U32(0x00000110L),U32(0x00080010L),U32(0x00080110L),
U32(0x01000010L),U32(0x01000110L),U32(0x01080010L),U32(0x01080110L),
U32(0x00200000L),U32(0x00200100L),U32(0x00280000L),U32(0x00280100L),
U32(0x01200000L),U32(0x01200100L),U32(0x01280000L),U32(0x01280100L),
U32(0x00200010L),U32(0x00200110L),U32(0x00280010L),U32(0x00280110L),
U32(0x01200010L),U32(0x01200110L),U32(0x01280010L),U32(0x01280110L),
U32(0x00000200L),U32(0x00000300L),U32(0x00080200L),U32(0x00080300L),
U32(0x01000200L),U32(0x01000300L),U32(0x01080200L),U32(0x01080300L),
U32(0x00000210L),U32(0x00000310L),U32(0x00080210L),U32(0x00080310L),
U32(0x01000210L),U32(0x01000310L),U32(0x01080210L),U32(0x01080310L),
U32(0x00200200L),U32(0x00200300L),U32(0x00280200L),U32(0x00280300L),
U32(0x01200200L),U32(0x01200300L),U32(0x01280200L),U32(0x01280300L),
U32(0x00200210L),U32(0x00200310L),U32(0x00280210L),U32(0x00280310L),
U32(0x01200210L),U32(0x01200310L),U32(0x01280210L),U32(0x01280310L),
],

#for D bits (numbered as per FIPS 46) 22 23 24 25 27 28
[
U32(0x00000000L),U32(0x04000000L),U32(0x00040000L),U32(0x04040000L),
U32(0x00000002L),U32(0x04000002L),U32(0x00040002L),U32(0x04040002L),
U32(0x00002000L),U32(0x04002000L),U32(0x00042000L),U32(0x04042000L),
U32(0x00002002L),U32(0x04002002L),U32(0x00042002L),U32(0x04042002L),
U32(0x00000020L),U32(0x04000020L),U32(0x00040020L),U32(0x04040020L),
U32(0x00000022L),U32(0x04000022L),U32(0x00040022L),U32(0x04040022L),
U32(0x00002020L),U32(0x04002020L),U32(0x00042020L),U32(0x04042020L),
U32(0x00002022L),U32(0x04002022L),U32(0x00042022L),U32(0x04042022L),
U32(0x00000800L),U32(0x04000800L),U32(0x00040800L),U32(0x04040800L),
U32(0x00000802L),U32(0x04000802L),U32(0x00040802L),U32(0x04040802L),
U32(0x00002800L),U32(0x04002800L),U32(0x00042800L),U32(0x04042800L),
U32(0x00002802L),U32(0x04002802L),U32(0x00042802L),U32(0x04042802L),
U32(0x00000820L),U32(0x04000820L),U32(0x00040820L),U32(0x04040820L),
U32(0x00000822L),U32(0x04000822L),U32(0x00040822L),U32(0x04040822L),
U32(0x00002820L),U32(0x04002820L),U32(0x00042820L),U32(0x04042820L),
U32(0x00002822L),U32(0x04002822L),U32(0x00042822L),U32(0x04042822L),
]

]