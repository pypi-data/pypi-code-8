"""
MPA FRONTEND
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""
import sys
import os
import mpa.mpa_core as MPA 

ccc = 1
file_config = sys.argv[ccc]
ccc += 1
if len(sys.argv) > 2:
	show_preview =  sys.argv[ccc]
else:
	show_preview = "no-preview"

if show_preview == "yes-preview":
	preview = True
else:
	preview = False

MPA.main(file_config, preview)



