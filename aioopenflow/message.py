import itertools
from aioopenflow.constants import *
from aioopenflow.types import Port

def is_msg(msg):
	"a check to see if the instance _msg_ is a subclass of aioopenflow.message.Message"
	try:
		return issubclass(msg.__class__, Message)
	except AttributeError:
		return False
#function:
make_xid = itertools.count(1).__next__

#baseclass:
class Message:
	version = None#set by protocol
	type = None#a MessageType
	xid = None
	data = b""
	def __init__(self, messagetype=None, *, xid=None, data=None):
		if self.type is None:
			assert type(messagetype) is MessageType
		if messagetype or self.type is None:
			self.type = messagetype
		if xid != None:
			self.xid = xid
		if data != None:
			assert type(data) is bytes
			self.data = data
	def __repr__(self):
		#if self.xid == None:
		#	self.xid = make_xid()
		
		if self.__class__.__name__ == "Message":
			return f"Message({self.type}, ver={self.version}, xid={self.xid})"
		else:
			return f"{self.__class__.__name__}(ver={self.version}, xid={self.xid})"
	__str__ =__repr__
	def pack(self):
		if self.xid == None:
			self.xid = make_xid()
		elif type(self.xid) is not int:
			self.xid = int(self.xid)
		
		assert type(self.data) is bytes
		assert type(self.type) is MessageType
		
		out = [
			bytes((self.version, self.type.for_version(self.version))),
			(len(self.data)+8).to_bytes(2, byteorder='big'),
			self.xid.to_bytes(4, byteorder='big'),
			self.data
		]
		
		return b"".join(out)
	def unpack(self, data):
		self.version = data[0]
		self.type = data[1]
		length = int.from_bytes(data[2:4], byteorder='big')
		self.xid = int.from_bytes(data[4:8], byteorder='big')
		self.data = data[8:8+length]
		
		#convert from int to MessageType
		self.type = getMessageType(self.version, self.type)

#childclasses
class MessageHello(Message):
	type = MT_Hello

class MessageError(Message):
	type = MT_Error
	def __init__(self, errorcode=None, errordata = b"", xid=None):
		if errorcode:
			assert type(errorcode) is ErrorCode
		if xid != None:
			self.xid = xid
		self.errorcode = errorcode
		self.errordata = errordata
	def data():
		def fget(self):#pack
			type, code = self.errorcode.for_version(self.version)
			out = (
				type.to_bytes(2, byteorder='big'),
				code.to_bytes(2, byteorder='big'),
				self.errordata,
			)
			return b"".join(out)
		def fset(self, value):#unpack
			type = int.from_bytes(value[0:2], byteorder='big')
			code = int.from_bytes(value[2:4], byteorder='big')
			
			self.errorcode = getErrorCode(self.version, type, code)
			self.errordata = value[4:]
		return locals()
	data = property(**data())

class MessageEchoReq(Message):
	type = MT_EchoReq 

class MessageEchoRes(Message):
	type = MT_EchoRes 

class MessageVendor(Message):
	type = MT_Vendor
	def vendor_id():
		def fget(self):
			return self.data[:4]
		def fset(self, value):
			self.data = value + self.data[4:]
		return locals()
	vendor_id = property(**vendor_id())
	type = MT_Vendor
	def vendor_data():
		def fget(self):
			return self.data[4:]
		def fset(self, value):
			self.data = self.data[:4] + value
		return locals()
	vendor_data = property(**vendor_data())

class MessageExperimenter(Message):
	type = MT_Experimenter 

class MessageFeatureReq(Message):
	type = MT_FeatureReq 

class MessageFeatureRes(Message):
	type = MT_FeatureRes
	
	datapath_id  = b"\x00"*8  #id/mac type-thing?
	n_buffers    = 0          #dentifies how many packets the switch can queue for PacketIn (capture and forward to the controller) activities
	n_tables     = 0          #The number of tables in the switch
	auxiliary_id = 0          #indicate how the switch is treating the OpenFlow transport channel (master controller, or auxiliary). Only used in openflow v1.3 and v1.4
	capabilities = frozenset()#capabilities supported by the switch
	actions      = frozenset()#actions supported by the switch, only used in openflow v1.0
	ports        = tuple()    #only used in openflow v1.0, v1.1 and v1.2
	
	def __str__(self):
		return f"MessageFeatureRes(ver={self.version}, xid={self.xid}) = {{datapath_id: {self.datapath_id}\n\tn_buffers: {self.n_buffers}\n\tn_tables: {self.n_tables}\n\tauxiliary_id: {self.auxiliary_id}\n\tcapabilities: {self.capabilities}\n\tactions: {self.actions}\n\tports: {self.ports}\n}}"

	def data():
		def fget(self):#pack
			assert type(self.datapath_id) is bytes, self.datapath_id
			assert len(self.datapath_id) == 8, self.datapath_id
			
			capabilities = sum(bit for bit, name in CA[self.version].items() if name in self.capabilities)
			actions      = sum(bit for bit, name in ACTIONS.items()          if name in self.actions)
			
			out = (
				self.datapath_id,
				self.n_buffers   .to_bytes(4, byteorder='big'),
				self.n_tables    .to_bytes(1, byteorder='big'),
				self.auxiliary_id.to_bytes(1, byteorder='big'),
				b"\0\0",
				capabilities     .to_bytes(4, byteorder='big'),
				actions          .to_bytes(4, byteorder='big'),
			)
			return b"".join(out)
			
		def fset(self, value):#unpack
			assert type(value) is bytes
			assert len(value) >= 24
			
			self.datapath_id  = int.from_bytes(value[ 0: 8], byteorder='big')
			self.n_buffers    = int.from_bytes(value[ 8:12], byteorder='big')
			self.n_tables     = value[12]
			self.auxiliary_id = value[13]
			c_flags           = int.from_bytes(value[16:20], byteorder='big')
			a_flags           = int.from_bytes(value[20:24], byteorder='big')
			port_data         = value[24:]
			
			self.capabilities = frozenset(CA[self.version][1<<i] for i in range(32) if c_flags & (1<<i))
			self.actions      = frozenset(ACTIONS[1<<i]          for i in range(32) if a_flags & (1<<i))
			
			if self.version <= openflow12:
				l = Port.length(self.version)
				self.ports = tuple(Port(self.version).unpack(port_data[l*i:l*i+l]) for i in range(len(port_data)//l))
			
		return locals()
	data = property(**data())

class MessageGetConfigReq(Message):
	type = MT_GetConfigReq 

class MessageGetConfigRes(Message):
	type = MT_GetConfigRes 

class MessageSetConfig(Message):
	type = MT_SetConfig 

class MessagePacketIn(Message):
	type = MT_PacketIn
	buffer_id   = -1
	total_len   = -1
	in_port     = -1
	reason      = -1
	packet_data = -1
	def data():
		def fget(self):
			raise NotImplementedError()
			out = (
				
			)
			return b"".join(out)
		def fset(self, value):
			assert self.version == openflow10
			
			self.buffer_id   = int.from_bytes(value[ 0: 4], byteorder='big', signed=True)
			self.total_len   = int.from_bytes(value[ 4: 6], byteorder='big')
			self.in_port     = int.from_bytes(value[ 6: 8], byteorder='big')
			self.reason      = int.from_bytes(value[ 8: 9], byteorder='big')
			self.packet_data = value[10:10+self.total_len]
			
			self.reason = ("NoMatch", "Action")[self.reason]
			
		return locals()
	data = property(**data())
	def __str__(self):
		return f"MessagePacketIn{(self.buffer_id, self.total_len, self.in_port, self.reason, self.packet_data)}"
	__repr__ = __str__
	
class MessageFlowRemoved(Message):
	type = MT_FlowRemoved 

class MessagePortStatus(Message):
	type = MT_PortStatus 

class MessagePacketOut(Message):
	type = MT_PacketOut
	buffer_id   = -1
	in_port     = 0xffff#None
	actions     = None#becomes a list
	packet_data = b""
	def __init__(self, *args, **kwargs):
		Message.__init__(self, *args, **kwargs)
		self.actions = []
	def from_PacketIn(self, msg):
		self.buffer_id   = msg.buffer_id
		self.in_port     = msg.in_port
		self.packet_data = msg.packet_data
	def data():
		def fget(self):
			assert self.version == openflow10
			assert type(self.packet_data) is bytes
			
			for i in self.actions:
				i.version = self.version
			
			actions = b"".join(i.pack() for i in self.actions)
			
			out = (
				self.buffer_id.to_bytes(4, byteorder='big', signed=True),
				self.in_port  .to_bytes(2, byteorder='big'),
				len(actions)  .to_bytes(2, byteorder='big'),
				actions,
				self.packet_data,
			)
			return b"".join(out)
		def fset(self, value):
			raise NotImplementedError()
		return locals()
	data = property(**data())
	def __str__(self):
		return f"MessagePacketOut{(self.buffer_id, self.in_port, self.actions, self.packet_data)}"
	__repr__ = __str__
	

class MessageFlowMod(Message):
	type = MT_FlowMod 

class MessagePortMod(Message):
	type = MT_PortMod 

class MessageGroupMod(Message):
	type = MT_GroupMod 

class MessageTableMod(Message):
	type = MT_TableMod 

class MessageStatsReq(Message):
	type = MT_StatsReq 

class MessageStatsRes(Message):
	type = MT_StatsRes 

class MessageBarrierReq(Message):
	type = MT_BarrierReq 

class MessageBarrierRes(Message):
	type = MT_BarrierRes 

class MessageMultipartReq(Message):
	type = MT_MultipartReq 

class MessageMultipartRes(Message):
	type = MT_MultipartRes 

class MessageQueueGetConfigReq(Message):
	type = MT_QueueGetConfigReq

class MessageQueueGetConfigRes(Message):
	type = MT_QueueGetConfigRes

class MessageRoleReq(Message):
	type = MT_RoleReq 

class MessageRoleRes(Message):
	type = MT_RoleRes 

class MessageGetAsyncReq(Message):
	type = MT_GetAsyncReq 

class MessageGetAsyncRes(Message):
	type = MT_GetAsyncRes 

class MessageSetAsync(Message):
	type = MT_SetAsync 

class MessageMeterMod(Message):
	type = MT_MeterMod 

class MessageTableStatus(Message):
	type = MT_TableStatus 

class MessageRoleStatus(Message):
	type = MT_RoleStatus 

class MessageRequestForward(Message):
	type = MT_RequestForward 

class MessageBundleControl(Message):
	type = MT_BundleControl 

class MessageBundleAddMessage(Message):
	type = MT_BundleAddMessage 	


MessageType_to_Message = {
	MT_Hello             : MessageHello,
	MT_Error             : MessageError,
	MT_EchoReq           : MessageEchoReq,
	MT_EchoRes           : MessageEchoRes,
	MT_Vendor            : MessageVendor,
	MT_Experimenter      : MessageExperimenter,
	MT_FeatureReq        : MessageFeatureReq,
	MT_FeatureRes        : MessageFeatureRes,
	MT_GetConfigReq      : MessageGetConfigReq,
	MT_GetConfigRes      : MessageGetConfigRes,
	MT_SetConfig         : MessageSetConfig,
	MT_PacketIn          : MessagePacketIn,
	MT_FlowRemoved       : MessageFlowRemoved,
	MT_PortStatus        : MessagePortStatus,
	MT_PacketOut         : MessagePacketOut,
	MT_FlowMod           : MessageFlowMod,
	MT_PortMod           : MessagePortMod,
	MT_GroupMod          : MessageGroupMod,
	MT_TableMod          : MessageTableMod,
	MT_StatsReq          : MessageStatsReq,
	MT_StatsRes          : MessageStatsRes,
	MT_BarrierReq        : MessageBarrierReq,
	MT_BarrierRes        : MessageBarrierRes,
	MT_MultipartReq      : MessageMultipartReq,
	MT_MultipartRes      : MessageMultipartRes,
	MT_QueueGetConfigReq : MessageQueueGetConfigReq,
	MT_QueueGetConfigRes : MessageQueueGetConfigRes,
	MT_RoleReq           : MessageRoleReq,
	MT_RoleRes           : MessageRoleRes,
	MT_GetAsyncReq       : MessageGetAsyncReq,
	MT_GetAsyncRes       : MessageGetAsyncRes,
	MT_SetAsync          : MessageSetAsync,
	MT_MeterMod          : MessageMeterMod,
	MT_TableStatus       : MessageTableStatus,
	MT_RoleStatus        : MessageRoleStatus,
	MT_RequestForward    : MessageRequestForward,
	MT_BundleControl     : MessageBundleControl,
	MT_BundleAddMessage  : MessageBundleAddMessage,
}
