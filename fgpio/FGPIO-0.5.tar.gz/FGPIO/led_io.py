#!/usr/bin/env python
# -*- coding:utf-8 -*

####################################
'''
# LED branchée sur un rpi_duino_io
# 
#    C'est vraiment pour faire jolie cette classe!!!
#
# AUTEUR : FredThx
#
# Projet : rpiduino_io
#
'''
#################################### 

import time
import functools
from rpiduino_io import *

#TODO : utiliser le mode PWM pour faire varier l'intensité lumineuse.
# voir en bas : début
# mais il faut plutôt créer des pin_io de type analogique output
# et bien gérer à la fois pcduino et Rpi

class led_io (device_io):
	''' LED branchée sur un rpiduino (pcduino ou Rpi)
	'''
	def __init__(self, pin=None):
		''' Initialisation
				pin	:	digital_pin_io
						(is None ou omis, la led est innactive
		'''
		if pin==None:
			self.pin = None
		else:
			if isinstance(pin, digital_pin_io):
				self.pin = pin
				self.pin.setmode(OUTPUT)
			else:
				raise rpiduino_io_error('argument erreur : n''est pas du type digital_pin_io')
		self.thread = None
		thread_end_time = None
		
	def none_none(fonction):
		'''Décorateur : si pin==None : la fonction ne s'applique pas
		'''
		@functools.wraps(fonction) # ca sert pour avoir un help(SBClient) utile
		def none_none_fonction(self, *args, **kwargs):
			if self.pin == None:
				return None
			else:
				return fonction(self, *args, **kwargs)
		return none_none_fonction
			
	@none_none
	def set(self, etat):
		''' change l'état de la LED
			etat	:	False / True
		'''
		if etat:
			self.pin.set(HIGH)
		else:
			self.pin.set(LOW)
	
	@none_none
	def get(self):
		''' Récupère l'état de la LED
		'''
		return self.pin.get()
	
	@none_none
	def on(self):
		''' Allume la LED
		'''
		self.set(True)
	
	@none_none
	def off(self):
		''' Eteint la LED
		'''
		self.set(False)
	
	@none_none
	def invert(self):
		'''Commute la LED
		'''
		self.pin.invert()
	
	@none_none
	def blink(self, time_on = 1, time_off = None, time_end = None):
		''' Create a thread for blinking the led
			- time_on	:	duration led is on (second)
			- time_off	:	duration led is off (second)
			- time_end	:	stop the thread after time_end seconds
							if time_end = None (default) the thread do not stop.
		'''
		self.th_time_on = time_on
		if time_off == None:
			self.th_time_off = time_on
		else:
			self.th_time_off = time_off
		if self.thread == None:
			self.thread = f_thread(self._blink)
			if time_end==None:
				self.thread_end_time = None
			else:
				self.thread_end_time = time.time() + time_end
			self.thread.start()

	def _blink(self):
		self.on()
		time.sleep(self.th_time_on)
		self.off()
		time.sleep(self.th_time_off)
		if self.thread_end_time!=None and time.time() > self.thread_end_time:
			self.stop()
	
	
	@none_none
	def stop(self):
		''' Stop blinking the led
		'''
		if self.thread:
			self.thread.stop()
			self.thread = None

# class pwm_led_io(device_io):
	# '''Une class pour piloter une led en PWM (Pulse Width Modulation
	# '''
	# def __init__(self, pin = None, intensite = 50, freq = 50):
		# '''Initialisation
			# - pin		:	digital_pin_io
			# - freq		:	frequency of the signal
			# - duty		:	%duration high
		# '''
		# if pin == None:
			# self.pin = None
		# else:
			# assert isinstance(pin, digital_pin_io), 'pin must be a digital_pin_io'
			# self.pin = pin
			# self.pin.setmode(PWM)
			
#########################################################
#                                                       #
#		EXEMPLE                                         #
#                                                       #
#########################################################

if __name__ == '__main__':
	import time
	pc = rpiduino_io()
	pin = pc.pin[40]
	LED = led_io(pin)
	none_led = led_io()
	LED.on()
	none_led.on() # Do nothing!
	time.sleep(1)
	LED.off()
	time.sleep(1)
	for i in range(0,5):
		LED.invert()
		print "la LED est " + str(LED.get())
		time.sleep(1)
	LED.blink()		# blink 1 second / 1 second
	time.sleep(5)
	LED.blink(0.1,0.2)	# Accelerate the blinking
	time.sleep(5)
	LED.stop()		# Stop the blinking
	