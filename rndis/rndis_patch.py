#!/usr/bin/python
# RNDIS bitrate patch for P4wnP1 by MaMe82
# author: Marcus Mengs (MaMe82)
#
# 
# Patch targets usb_f_rndis.ko on Raspbian with kernel 4.4.50+
#
# As the whole code is position independant, the patch could possibly apply to other
# versions of the kernel module - USE IT AT YOUR OWN RISK

import struct
import sys

src_file="usb_f_rndis.ko.orig"
dst_file="usb_f_rndis.ko.patched"
target_bitrate=20000000000

# build binary patch

# old code:
#  cmp r2, 5
#  beq 0x8000554
#  cmp r2, 3
#  movne r2, 0x17c00
#  moveq r2, 0x410000
#  mov r1, 0
old_code = "\x05\x00\x52\xe3\x0c\x00\x00\x0a\x03\x00\x52\xe3\x5f\x2b\xa0\x13\x41\x28\xa0\x03\x00\x10\xa0\xe3"

# new code:
#  cmp r2, 5
#  mov r0, r0
#  ldr r0, [pc]
#  b 8
#  .word <target bitrate>
#  mov r1, 0

uint32_bitrate = struct.pack("<i", target_bitrate/100) # bitrate in 100bps measure, converted to little endian
new_code = "\x05\x00\x52\xe3\x00\x00\xa0\xe1\x00\x20\x9f\xe5\x00\x00\x00\xea"
new_code += uint32_bitrate
new_code += "\x00\x10\xa0\xe3"


print "RNDIS composite function bitrate patch for Raspbian @kernel 4.4.50+"
print "by MaMe82"
print "==================================================================="
print ""

with open(src_file, "rb") as f:
	a = f.read()

if not old_code in a:
	print "[ERROR] Sorry, '" + src_file + "' isn't patchable. Wrong file version?"
	sys.exit(0)
else:	
	print "..Patching '" + src_file + "' ..."
	patched = a.replace(old_code, new_code)
	print "..Writing patched file '" + dst_file + "' ..."
	with open(dst_file, "wb") as f:
		f.write(patched)
	print "..Finishhed"
	sys.exit(1)
