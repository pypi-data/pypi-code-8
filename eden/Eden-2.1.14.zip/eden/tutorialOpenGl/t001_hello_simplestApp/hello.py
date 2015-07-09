# Copyright (C) 2005 - 2014 Jacques de Hooge, Geatec Engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.

# hello.py

from org.qquick.eden import *

import sdl2

testString = 'THE QUICK BROWN\nFOX JUMPS OVER\nTHE LAZY DOG\naap noot mies wim zus jet teun vuur gijs lam kees bok weide does hok duif schapen\n'

sizeNode = Node ([0.2, 0.2, 0.2])
textNode = Node (testString)
text2Node = Node ('')

fontNode = Node ({'name': 'arial', 'points': 32})

buttonTextNode = Node ()
buttonPressedNode = Node (None)
buttonTextNode.dependsOn ([buttonPressedNode], lambda: 'Thanks' if buttonPressedNode.new else 'Press me')
buttonView = ButtonView (textNode = buttonTextNode, fontNode = fontNode, panelColorNode = [0., 0., 1.], textColorNode = [1., 1., 1.], pressedNode = buttonPressedNode)

editView = EditView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 1., 0.5], textColorNode = [0., 0., 1.])

mainView = MainView (	
	clientView = BeamView (childViews = [
		GridView (childViews = [
			[
				buttonView,
				EditView (textNode = textNode, fontNode = fontNode, panelColorNode = [0., 1., 1.], textColorNode = [0., 0., 0.]), 2, 
				LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 1., 1.], textColorNode = [0., 0., 0.]),
			],
			[
				LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 0.5, 1.], textColorNode = [1., 1., 0.]),
				editView, 2,
				LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [0., 0., 0.], textColorNode = [0., 0., 1.])
			], 2, 
			[
				LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 0., 1.], textColorNode = [1., 1., 0.]),
				LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 1., 0.], textColorNode = [0., 0., 1.]),
				LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 0.5, 0.5], textColorNode = [0., 0., 1.]), 2
			]
		]),
		LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 1., 0.], textColorNode = [0., 0., 1.]), 
		LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [0., 1., 0.], textColorNode = [1., 0., 0.]),
		LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 0., 0.], textColorNode = [0., 1., 0.]),
		LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [1., 1., 1.], textColorNode = [0., 0., 0.]),
		LabelView (textNode = textNode, fontNode = fontNode, panelColorNode = [0., 0., 0.], textColorNode = [1., 1., 1.])
	]),
	sizeNode = sizeNode,
	colorNode = [0.5, 0.4, 0.2]
)

# editView.labelView.textView.cursorHitOffsetNode.trace ('cursorHitOffsetNode')

mainView.execute ()
