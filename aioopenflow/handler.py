from aioopenflow.constants import *
from aioopenflow.message import *

import logging
logger = logging.getLogger('aioopenflow')

class BaseHandler:#handles establishing and maintaining a connection
	#constants
	protocol = None
	loop = None
	version = None#set when hello sequence has finished
	#class specific
	supported_versions = frozenset((openflow10, openflow11, openflow12, openflow13, openflow14))
	#state:
	switch_datapath_id  = -1         #id/mac type-thing?
	switch_n_buffers    = 0          #dentifies how many packets the switch can queue for PacketIn (capture and forward to the controller) activities
	switch_n_tables     = 0          #The number of tables in the switch
	switch_auxiliary_id = 0          #indicate how the switch is treating the OpenFlow transport channel (master controller, or auxiliary). Only used in openflow v1.3 and v1.4
	switch_capabilities = frozenset()#capabilities supported by the switch
	switch_actions      = frozenset()#actions supported by the switch, only used in openflow v1.0
	switch_ports        = None       #only used in openflow v1.0, v1.1 and v1.2
	def __init__(self, protocol, loop):
		self.protocol = protocol
		self.loop = loop
		
		self.switch_ports = {}#[port_id] = Port()
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
		
		if self.switch_datapath_id == -1:
			logger.info(f"connection successfully established with {self.protocol.peername}")
			self.loop.call_soon(self.connection_established)
			
		self.switch_datapath_id  = msg.datapath_id
		self.switch_n_buffers    = msg.n_buffers
		self.switch_n_tables     = msg.n_tables
		self.switch_auxiliary_id = msg.auxiliary_id
		self.switch_capabilities = msg.capabilities
		self.switch_actions      = msg.actions
		self.switch_ports        = {i.port_id : i for i in msg.ports}
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
		#print(msg.port)
		if msg.reason in ("Add", "Modify"):
			self.switch_ports[msg.port.port_id] = msg.port
		elif msg.reason == "Delete":
			if msg.port.port_id in self.switch_ports:
				del self.switch_ports[msg.port.port_id]
		else:
			raise ValueError(f"handler.handle_PortStatus got msg.reason == {msg.reason}")
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
