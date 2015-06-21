#! /usr/bin/env python

# From http://www.reportlab.com/documentation/faq/#2.1.2

import hashlib

import reportlab.rl_settings
reportlab.rl_settings.invariant = True

dstf = "hello.pdf"

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
c = canvas.Canvas(dstf)
c.drawString(9*cm, 22*cm, "Hello World!")
c.showPage()
c.save()

print (hashlib.md5(open(dstf, 'rb').read()).hexdigest())
