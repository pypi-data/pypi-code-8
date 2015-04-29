from commands_proto import *

class NRF24L01():
	#Commands
	R_REG = 0x00
	W_REG = 0x20
	RX_PAYLOAD = 0x61
	TX_PAYLOAD = 0xA0
	FLUSH_TX = 0xE1
	FLUSH_RX = 0xE2
	ACTIVATE = 0x50
	R_STATUS = 0xFF

	#Registers
	NRF_CONFIG = 0x00
	EN_AA = 0x01
	EN_RXADDR = 0x02
	SETUP_AW = 0x03
	SETUP_RETR = 0x04
	RF_CH = 0x05
	RF_SETUP = 0x06
	NRF_STATUS = 0x07
	OBSERVE_TX = 0x08
	CD = 0x09
	RX_ADDR_P0 = 0x0A
	RX_ADDR_P1 = 0x0B
	RX_ADDR_P2 = 0x0C
	RX_ADDR_P3 = 0x0D
	RX_ADDR_P4 = 0x0E
	RX_ADDR_P5 = 0x0F
	TX_ADDR = 0x10
	RX_PW_P0 = 0x11
	RX_PW_P1 = 0x12
	RX_PW_P2 = 0x13
	RX_PW_P3 = 0x14
	RX_PW_P4 = 0x15
	RX_PW_P5 = 0x16
	FIFO_STATUS = 0x17
	DYNPD = 0x1C
	FEATURE = 0x1D
	def __init__(self,H):
		self.H = H
	"""
	routines for the NRFL01 radio
	"""
	def init(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_SETUP)
		self.H.__get_ack__()
		
	def rxmode(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_RXMODE)
		self.H.__get_ack__()
		
	def txmode(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_TXMODE)
		self.H.__get_ack__()
		
	def power_down(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_POWERDOWN)
		self.H.__get_ack__()
		
	def rxchar(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_RXCHAR)
		value = self.H.__getByte__()
		self.H.__get_ack__()
		return value
		
	def txchar(self,char):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_TXCHAR)
		self.H.__sendByte__(char)
		self.H.__get_ack__()
		
	def hasdata(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_HASDATA)
		value = self.H.__getByte__()
		self.H.__get_ack__()
		return value
		
	def flush(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_FLUSH)
		self.H.__get_ack__()

	def write_register(self,address,value):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_WRITEREG)
		self.H.__sendByte__(address)
		self.H.__sendByte__(value)
		self.H.__get_ack__()

	def read_register(self,address):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_READREG)
		self.H.__sendByte__(address)
		val=self.H.__getByte__()
		self.H.__get_ack__()
		return val

	def get_status(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_GETSTATUS)
		val=self.H.__getByte__()
		self.H.__get_ack__()
		return val

	def write_command(self,cmd):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_WRITECOMMAND)
		self.H.__sendByte__(cmd)
		self.H.__get_ack__()

