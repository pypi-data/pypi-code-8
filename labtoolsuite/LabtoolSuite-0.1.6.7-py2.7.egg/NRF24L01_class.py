from commands_proto import *

class NRF24L01():
	#Commands
	R_REG = 0x00
	W_REG = 0x20
	RX_PAYLOAD = 0x61
	TX_PAYLOAD = 0xA0
	ACK_PAYLOAD = 0xA8
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
	R_RX_PL_WID = 0x60
	FIFO_STATUS = 0x17
	DYNPD = 0x1C
	FEATURE = 0x1D
	PAYLOAD_SIZE = 0
	ACK_PAYLOAD_SIZE =0
	READ_PAYLOAD_SIZE =0	
	
	def __init__(self,H):
		self.H = H
	"""
	routines for the NRFL01 radio
	"""
	def init(self):
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_SETUP)
		self.H.__get_ack__()
		time.sleep(0.15) #15 mS settling time
		
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
		return self.H.__get_ack__()>>4
		
	def hasData(self):
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

	def write_address(self,register,address):
		'''
		register can be TX_ADDR, RX_ADDR_P0 -> RX_ADDR_P5
		3 byte address.  eg 0xFFABXX . XX cannot be FF
		
		'''
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_WRITEADDRESS)
		self.H.__sendByte__(register)
		self.H.__sendByte__(address&0xFF);self.H.__sendByte__((address>>8)&0xFF);
		self.H.__sendByte__((address>>16)&0xFF);
		self.H.__get_ack__()

	def init_shockburst_transmitter(self,**args):
		self.PAYLOAD_SIZE=args.get('PAYLOAD_SIZE',self.PAYLOAD_SIZE)
		myaddr=args.get('myaddr',0xA523B5)
		sendaddr=args.get('sendaddr',0xA523B5)

		self.init()
		self.write_register(self.RF_CH,10)
		self.write_register(self.RF_SETUP,0x26)  #2MBPS speed
		#shockburst
		self.write_address(self.TX_ADDR,sendaddr)     #send to node with this address
		self.write_address(self.RX_ADDR_P0,myaddr)	#transmitter's address
		self.write_register(self.EN_AA,0x01) #enable auto Acknowledge
		self.write_register(self.DYNPD,0x01) #enable dynamic payload on Data pipe P0
		self.write_register(self.FEATURE,0x06) #enable dynamic payload length
		self.write_register(self.SETUP_RETR,0x55) #500uS retransmit delay. 5 retransmit
		self.write_register(self.RX_PW_P0,10) 
		self.txmode()
		time.sleep(0.1)
		self.flush()

		#---------

	def init_shockburst_receiver(self,**args):
		self.PAYLOAD_SIZE=args.get('PAYLOAD_SIZE',self.PAYLOAD_SIZE)
		myaddr=args.get('myaddr',0xA523B5)
		sendaddr=args.get('sendaddr',0xA523B5)
		self.init()
		self.write_register(self.RF_CH,10)
		self.write_register(self.RF_SETUP,0x26)  #2MBPS speed

		self.write_address(self.TX_ADDR,sendaddr)     #send to node with this address
		self.write_address(self.RX_ADDR_P0,myaddr)	#will receive the ACK Payload from that node
		enabled_pipes = 1				#pipe 0 enabled
		for a in range(1,6):
			x=args.get('myaddr'+str(a),None)
			if x: 
				print hex(x),hex(self.RX_ADDR_P0+a)
				enabled_pipes|= (1<<a)
				self.write_address(self.RX_ADDR_P0+a,x)
		P15_base_address = args.get('myaddr1',None)
		if P15_base_address: self.write_address(self.RX_ADDR_P1,P15_base_address)

		self.write_register(self.EN_RXADDR,enabled_pipes) #enable pipes
		self.write_register(self.EN_AA,enabled_pipes) #enable auto Acknowledge on all pipes
		self.write_register(self.DYNPD,enabled_pipes) #enable dynamic payload on Data pipes
		self.write_register(self.FEATURE,0x06) #enable dynamic payload length
		#self.write_register(self.RX_PW_P0,self.PAYLOAD_SIZE)

		self.rxmode()
		time.sleep(0.1)
		self.flush()


	def init_transmitter(self,**args):
		self.PAYLOAD_SIZE=args.get('PAYLOAD_SIZE',self.PAYLOAD_SIZE)
		myaddr=args.get('myaddr',0xA523B5)
		sendaddr=args.get('sendaddr',0xA523B5)

		self.init()
		self.write_register(self.RF_CH,10)
		self.write_register(self.RF_SETUP,0x26)  #2MBPS speed
		#shockburst
		self.write_address(self.TX_ADDR,sendaddr)     #send to node with this address
		self.write_address(self.RX_ADDR_P0,myaddr)	#transmitter's address
		self.write_register(self.EN_AA,0x01) #enable auto Acknowledge
		self.write_register(self.DYNPD,0x00) #enable dynamic payload on Data pipe P0
		self.write_register(self.FEATURE,0x00) #enable dynamic payload length
		self.write_register(self.SETUP_RETR,0x00) #500uS retransmit delay. 5 retransmit
		self.txmode()
		time.sleep(0.1)
		self.flush()

		#---------

	def init_receiver(self,**args):
		self.PAYLOAD_SIZE=args.get('PAYLOAD_SIZE',self.PAYLOAD_SIZE)
		myaddr=args.get('myaddr',0xA523B5)
		sendaddr=args.get('sendaddr',0xA523B5)
		self.init()
		self.write_register(self.RF_CH,10)
		self.write_register(self.RF_SETUP,0x26)  #2MBPS speed

		self.write_address(self.TX_ADDR,sendaddr)     #send to node with this address
		self.write_address(self.RX_ADDR_P0,myaddr)	#will receive the ACK Payload from that node
		enabled_pipes = 1				#pipe 0 enabled
		for a in range(1,6):
			x=args.get('myaddr'+str(a),None)
			if x: 
				print hex(x),hex(self.RX_ADDR_P0+a)
				enabled_pipes|= (1<<a)
				self.write_address(self.RX_ADDR_P0+a,x)
		P15_base_address = args.get('myaddr1',None)
		if P15_base_address: self.write_address(self.RX_ADDR_P1,P15_base_address)

		self.write_register(self.EN_RXADDR,enabled_pipes) #enable pipes
		self.write_register(self.EN_AA,enabled_pipes) #auto Acknowledge on no pipes
		self.write_register(self.DYNPD,0x00) #dynamic payload on no Data pipes
		self.write_register(self.FEATURE,0x00) #disable dynamic payload length
		self.write_register(self.RX_PW_P0,self.PAYLOAD_SIZE)

		self.rxmode()
		time.sleep(0.1)
		self.flush()


	def read_payload(self,numbytes):
		if(numbytes!=self.READ_PAYLOAD_SIZE):
			self.READ_PAYLOAD_SIZE=numbytes
			if self.READ_PAYLOAD_SIZE>32:
				print 'too large. reading 32.'
				self.READ_PAYLOAD_SIZE=32
				numbytes=32
			else:
				self.write_register(self.RX_PW_P0,self.READ_PAYLOAD_SIZE)
				print 'read payload size:',self.READ_PAYLOAD_SIZE
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_READPAYLOAD)
		self.H.__sendByte__(numbytes)
		data=self.H.fd.read(numbytes)
		self.H.__get_ack__()
		return [ord(a) for a in data]


	def write_payload(self,data): 
		if(len(data)!=self.PAYLOAD_SIZE):
			self.PAYLOAD_SIZE=len(data)
			if self.PAYLOAD_SIZE>32:
				print 'too large. truncating.'
				self.PAYLOAD_SIZE=32
				data=data[:32]
			else:
				self.write_register(self.RX_PW_P0,self.PAYLOAD_SIZE)
				print 'tx payload size:',self.PAYLOAD_SIZE
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_WRITEPAYLOAD)
		self.H.__sendByte__(len(data)|0x80)  #0x80 implies transmit immediately. Otherwise it will simply load the TX FIFO
		self.H.__sendByte__(self.TX_PAYLOAD)
		for a in data:
			self.H.__sendByte__(a)
		return self.H.__get_ack__()>>4

	
	def write_ack_payload(self,data,pipe): 
		if(len(data)!=self.ACK_PAYLOAD_SIZE):
			self.ACK_PAYLOAD_SIZE=len(data)
			if self.ACK_PAYLOAD_SIZE>15:
				print 'too large. truncating.'
				self.ACK_PAYLOAD_SIZE=15
				data=data[:15]
			else:
				print 'ack payload size:',self.ACK_PAYLOAD_SIZE
		self.H.__sendByte__(NRFL01)
		self.H.__sendByte__(NRF_WRITEPAYLOAD)
		self.H.__sendByte__(len(data))
		self.H.__sendByte__(self.ACK_PAYLOAD|pipe)
		for a in data:
			self.H.__sendByte__(a)
		return self.H.__get_ack__()>>4
	
	
	
	
	
