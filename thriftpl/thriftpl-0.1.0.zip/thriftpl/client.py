# -*- coding: utf-8 -*-
from __future__ import with_statement

import Queue
from threading import Lock
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

from thrift.Thrift import TApplicationException

DEBUG = False

class SyncDict(object):
	def __init__(self):
		self.__ctn={}
		self.__lock=Lock()
		
	def put(self,key,value):
		self.__lock.acquire()
		try:
			self.__ctn[key]=value
		finally:
			self.__lock.release()
		
	def get(self,key):
		self.__lock.acquire()
		try:
			return self.__ctn.get(key)
		finally:
			self.__lock.release()
			
	def pop(self,key):
		self.__lock.acquire()
		try:
			self.__ctn.pop(key)
		finally:
			self.__lock.release()
		
	def size(self):
		self.__lock.acquire()
		try:
			return len(self.__ctn)
		finally:
			self.__lock.release()
	


class ThriftClientConfig(object):
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

class ThriftClientPool(object):
	def __init__(self,clientConfig=None, maxPoolSize=10,maxWait=500,timeout=5000,
				 clientInterface=None, serviceName=None, protocol=TBinaryProtocol,
				 framed=True):
		"""
		clientConfig: object for ThriftClientConfig
		maxPoolSize: max size of pooled clients ,default is 10
		maxWait: max time for waiting to acquire a  client ,unit ms
		timeout: socket timeout for client ,unit ms
		clientInterface: thrift client interface class
		serviceName: for TMultiplexedProtocol ,needs serviceName to invoke specify service
		protocol: thrift protocols ,default is TBinaryProtocol
		framed: use framed transport,defautl is True
		"""
		# for config in configs :
		if not isinstance(clientConfig, ThriftClientConfig):
			raise Exception("clientConfig must be object of ThriftPoolConfig")
		if clientInterface is None:
			raise Exception("clientConfig must be object of ThriftPoolConfig")
		self.maxPoolSize=maxPoolSize
		self.maxWait =maxWait/1000.0
		self.clientConfig= clientConfig
		self.timeout=timeout
		self.clientInterface = clientInterface
		self.serviceName=serviceName
		self.protocol= protocol
		self.framed=framed
		
		self._initPool()

	def _initPool(self):
		self.__avalible_pool = Queue.LifoQueue(self.maxPoolSize)
		self.__busi_client=SyncDict()

	def __makeObject(self):
		return ThriftClient(self.clientConfig.ip, self.clientConfig.port, timeout=self.timeout,
							clientInterface=self.clientInterface, serviceName=self.serviceName,
							protocol=self.protocol, framed=self.framed)

	def returnObject(self, thriftClient):
		if thriftClient is not None:
			cid = id(thriftClient)
			try:
				self.__busi_client.pop(cid)
			except :
				pass
			try:
				self.__avalible_pool.put(thriftClient)
			except:
				thriftClient.close()
				

	def brokenObject(self, thriftClient):
		if thriftClient is not None:
			cid = id(thriftClient)
			try:
				self.__busi_client.pop(cid)
			except :
				pass
			try:
				thriftClient.close()
			except:
				pass
			

	def borrowObject(self):
		client = None
		try:
			client = self.__avalible_pool.get(timeout=self.maxWait)
		except :
			client =None
		
		if client is None :
			client = self.__makeObject()
		
		if client is not None:
			self.__busi_client.put(id(client),client)
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
