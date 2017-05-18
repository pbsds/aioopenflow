from aioopenflow.constants import *
from aioopenflow.message import *

import logging
logger = logging.getLogger('aioopenflow')

class BaseHandler:#handles the HELLO sequence
	#constants
	protocol = None
	loop = None
	version = None#set when hello sequence has finished
	switch_ports = []#not yet implemented
	switch_mac = None#not yet implemented
	#class specific
	supported_versions = frozenset((openflow10, openflow11, openflow12, openflow13, openflow14))
	FeatureRes = None
	def __init__(self, protocol, loop):
		self.protocol = protocol
		self.loop = loop
	def connection_made(self):
		msg = MessageHello()
		msg.version = max(self.supported_versions)
		
		self.protocol.send_message(msg)
	def connection_established(self):
		pass
	def connection_lost(self, exc):
		pass
	def handle_message(self, msg):
		logger.debug(f"{self.__class__.__name__}.handle_{msg.type.name}( {msg} )")
		return getattr(self, f"handle_{msg.type.name}")(msg)
	
	#a handler for each message type:
	def handle_Hello(self, msg):#doesn't handle openflow 1.3.1+ bitmasks
		if self.version != None:
			self.protocol.send_error_message(ER_HelloFailed.EPerm, msg.xid)
			
		elif msg.version not in self.supported_versions:
			self.protocol.send_error_message(ER_HelloFailed.Incompatible, msg.xid, version = msg.version)
			
		else:
			self.version = msg.version
			logger.info(f"{self.__class__.__name__} set to version={self.version}")
			
			self.protocol.send_message(MessageFeatureReq())
	def handle_Error(self, msg):
		logger.error(f"{self.__class__.__name__}.handle_Error got a {msg.errorcode}")
		
		if msg.errorcode == ER_HelloFailed.Incompatible:
			pass
		else:
			raise NotImplementedError()
	def handle_EchoReq(self, msg):
		self.protocol.send_message(MessageEchoRes(data=msg.data, xid=msg.xid))
	def handle_EchoRes(self, msg):
		raise NotImplementedError()
	def handle_Vendor(self, msg):
		raise NotImplementedError()
	def handle_Experimenter(self, msg):
		raise NotImplementedError()
	def handle_FeatureReq(self, msg):
		self.protocol.send_error_message(ER_BadAction.BadType, msg.xid)
	def handle_FeatureRes(self, msg):
		if not self.version:
			logger.error("Recieved a FeatureRes before version was chosen")
			self.protocol.send_error_message(ER_BadRequest.BadType, msg.xid, version = msg.version)
		#logger.info(str(msg))
		#raise NotImplementedError()
		if not self.FeatureRes:
			self.FeatureRes = msg
			logger.info(f"connection successfully established with {self.protocol.peername}")
			self.loop.call_soon(self.connection_established)
		else:
			self.FeatureRes = msg
	def handle_GetConfigReq(self, msg):
		raise NotImplementedError()
	def handle_GetConfigRes(self, msg):
		raise NotImplementedError()
	def handle_SetConfig(self, msg):
		raise NotImplementedError()
	def handle_PacketIn(self, msg):
		raise NotImplementedError()
	def handle_FlowRemoved(self, msg):
		raise NotImplementedError()
	def handle_PortStatus(self, msg):
		raise NotImplementedError()
	def handle_PacketOut(self, msg):
		raise NotImplementedError()
	def handle_FlowMod(self, msg):
		raise NotImplementedError()
	def handle_PortMod(self, msg):
		raise NotImplementedError()
	def handle_GroupMod(self, msg):
		raise NotImplementedError()
	def handle_TableMod(self, msg):
		raise NotImplementedError()
	def handle_StatsReq(self, msg):
		raise NotImplementedError()
	def handle_StatsRes(self, msg):
		raise NotImplementedError()
	def handle_BarrierReq(self, msg):
		raise NotImplementedError()
	def handle_BarrierRes(self, msg):
		raise NotImplementedError()
	def handle_MultipartReq(self, msg):
		raise NotImplementedError()
	def handle_MultipartRes(self, msg):
		raise NotImplementedError()
	def handle_QueueGetConfigReq(self, msg):
		raise NotImplementedError()
	def handle_QueueGetConfigRes(self, msg):
		raise NotImplementedError()
	def handle_RoleReq(self, msg):
		raise NotImplementedError()
	def handle_RoleRes(self, msg):
		raise NotImplementedError()
	def handle_GetAsyncReq(self, msg):
		raise NotImplementedError()
	def handle_GetAsyncRes(self, msg):
		raise NotImplementedError()
	def handle_SetAsync(self, msg):
		raise NotImplementedError()
	def handle_MeterMod(self, msg):
		raise NotImplementedError()
	def handle_RoleStatus(self, msg):
		raise NotImplementedError()
	def handle_TableStatus(self, msg):
		raise NotImplementedError()
	def handle_RequestForward(self, msg):
		raise NotImplementedError()
	def handle_BundleControl(self, msg):
		raise NotImplementedError()
	def handle_BundleAddMessage(self, msg):
		raise NotImplementedError()
