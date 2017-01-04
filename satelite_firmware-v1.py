#!/usr/bin/python
# -*- coding: utf-8 -*-

import zlib
import zipfile
import binascii
import itertools

def getcrc_hex(instr):
  ret=binascii.crc32(instr);
  return "%X"% (ret & 0xffffffff);

# extracting: flag.txt                 bad CRC 5aaf1344  (should be 5c671a32)
flag_bad='CTF{ZZZZZZf057b0ba16c542d80c31c8c05d}';
flag_crc='5c671a32'

crc= binascii.crc32(flag_bad);
crc=format(crc & 0xFFFFFFFF, '08x')


#print(crc_int);
for it in itertools.product('0123456789abcdef',repeat=6):
  flag_tst = flag_bad.replace('ZZZZZZ',''.join(it) );
  this_crc = format(zlib.crc32( flag_tst ) & 0xFFFFFFFF, '08x');
#  print(this_crc);
  if (flag_crc==this_crc):
    print('FOUND');
    print(flag_tst);
    print(it);
print('done');

