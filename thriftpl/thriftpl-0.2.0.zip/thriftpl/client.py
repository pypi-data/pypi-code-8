# -*- coding: utf-8 -*-
from __future__ import with_statement

import Queue
from multiprocessing import Semaphore
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

from thrift.Thrift import TApplicationException

DEBUG = False

class HostAndPort(object):
	def __init__(self, ip=None, port=None, weight=0):
		self._ip = ip
		self._port = port
		self._weight = weight

	@property
	def weight(self):
		return self._weight

	@property
	def ip(self):
		return self._ip

	@property
	def port(self):
		return self._port
		
class ThriftClientConfig(object):
	def __init__(self,clientInterface=None,protocol=TBinaryProtocol,framed=True,timeout=5000,serviceName=None):
		self._timeout=timeout
		if clientInterface is None:
			raise Exception("clientInterface cannot be None")
		self._clientInterface = clientInterface
		self._serviceName=serviceName
		self._protocol= protocol
		self._framed=framed

	@property
	def timeout(self):
		return self._timeout
	
	@property
	def clientInterface(self):
		return self._clientInterface
		
	@property
	def protocol(self):
		return self._protocol
		
	@property
	def framed(self):
		return self._framed
		
	@property
	def serviceName(self):
		return self._serviceName
		
class ThriftPoolConfig(object):
	def __init__(self,minPoolSize=1,maxPoolSize=10,maxWait=500):
		self._minPoolSize=minPoolSize
		self._maxPoolSize=maxPoolSize
		self._maxWait=maxWait
	
	@property
	def minPoolSize(self):
		return self._minPoolSize
		
	@property
	def maxPoolSize(self):
		return self._maxPoolSize
		
	@property
	def maxWait(self):
		return self._maxWait

class ThriftClientPool(object):
	def __init__(self,clientConfig=None,poolConfig=None,address=None):
		"""
		clientConfig: object for ThriftClientConfig
		poolConfig: object for ThriftPoolConfig
		timeout: socket timeout for client ,unit ms
		clientInterface: thrift client interface class
		serviceName: for TMultiplexedProtocol ,needs serviceName to invoke specify service
		protocol: thrift protocols ,default is TBinaryProtocol
		framed: use framed transport,defautl is True
		"""
		# for config in configs :
		if not isinstance(clientConfig, ThriftClientConfig):
			raise Exception("clientConfig must be object of ThriftPoolConfig")
		if not isinstance(address, HostAndPort):
			raise Exception("address must be object of HostAndPort")
		if poolConfig is None:
			poolConfig =ThriftPoolConfig()
		if not isinstance(poolConfig,ThriftPoolConfig):
			raise Exception("poolConfig must be object of ThriftPoolConfig")
		self.poolConfig = poolConfig
		self.clientConfig= clientConfig
		self.address=address
		
		self._initPool()

	def _initPool(self):
		self.__semaphore = Semaphore(self.poolConfig.maxPoolSize)
		self.__avalible_pool = Queue.LifoQueue(self.poolConfig.maxPoolSize)
		self.__using=[]
		for i in range(self.poolConfig.minPoolSize):
			self.__avalible_pool.put(self.__makeObject())

	def __makeObject(self):
		return ThriftClient(self.address.ip, self.address.port, timeout=self.clientConfig.timeout,
							clientInterface=self.clientConfig.clientInterface, serviceName=self.clientConfig.serviceName,
							protocol=self.clientConfig.protocol, framed=self.clientConfig.framed)

	def returnObject(self, thriftClient):
		if thriftClient is not None:
			try:
				self.__avalible_pool.put(thriftClient)
				self.__using.remove(thriftClient)
			except :
				pass
			finally:
				self.__semaphore.release()
				
	def brokenObject(self, thriftClient):
		if thriftClient is not None:
			try:
				try:
					thriftClient.close()
				except:
					pass
				self.__using.remove(thriftClient)
			except :
				pass
			finally:
				self.__semaphore.release()
			
	def borrowObject(self):
		client= None
		if self.__semaphore.acquire(block=True,timeout=self.poolConfig.maxWait):
			try:
				try:
					client = self.__avalible_pool.get(timeout=self.poolConfig.maxWait)
				except :
					client =None
				if client is None:
					if len(self.__using)<self.poolConfig.maxPoolSize:
						client=self.__makeObject()
			finally:
				if client is None:
					self.__semaphore.release()
				else :
					self.__using.append(client)
		return client

	def getClient(self):
		return self._ClientProxy(self)

	class _ClientProxy(object):
		def __init__(self, pool):
			self._pool = pool

		def __getattr__(self, method):
			return MethodInvoker(self._pool, method)


class MethodInvoker(object):
	def __init__(self, pool, method):
		self._pool = pool
		self._method = method

	def __call__(self, *args, **argsmap):
		client = None
		try:
			client = self._pool.borrowObject()
			func = getattr(client, self._method)
			return func(*args, **argsmap)
		except TApplicationException as te:
			if te.type == te.MISSING_RESULT:
				return None
			raise te
		except Exception as e:
			if client:
				self._pool.brokenObject(client)
				client =None
			raise e
		finally:
			if client:
				self._pool.returnObject(client)


class ThriftClient(object):
	def __init__(self, ip=None, port=None, timeout=5000, clientInterface=None, serviceName=None,
				 protocol=TBinaryProtocol, framed=True):
		self._ip = ip
		self._port = port
		self._timeout = timeout
		self._client = clientInterface
		self._clientObj = None
		self._transport = None
		self._serviceName = serviceName
		self._protocol = protocol
		self._framed = framed

	def __getattr__(self, method):
		return self._RemoteInterface(self.get_client(), method)

	def get_client(self):
		if (None != self._clientObj):
			return self._clientObj
		else:
			if (None != self._client ):
				transport = TSocket.TSocket(self._ip, self._port)
				transport.setTimeout(self._timeout)
				if self._framed:
					transport = TTransport.TFramedTransport(transport)
				protocol = self._protocol(transport)
				if None != self._serviceName:
					multiplexed= False
					try :
						from thrift.protocol import TMultiplexedProtocol
						multiplexed = True
					except :
						pass
					if multiplexed :
						protocol = TMultiplexedProtocol(protocol, self._serviceName)
				self._transport = transport
				self.open()
				self._clientObj = self._client(protocol)
				return self._clientObj
			else:
				return None


	def open(self):
		if (None != self._transport):
			self._transport.open()

	def close(self):
		if (None != self._transport):
			self._transport.close()

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close()

	class _RemoteInterface(object):
		def __init__(self, client, method):
			self._client = client
			self._method = method

		def __call__(self, *args, **argmap):
			return getattr(self._client, self._method)(*args, **argmap)
