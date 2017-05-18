import aioopenflow.constants
import aioopenflow.types
import logging
logger = logging.getLogger('aioopenflow')
#http://flowgrammable.org/sdn/openflow/message-layer/action/
#http://ryu.readthedocs.io/en/latest/ofproto_v1_0_ref.html#action-structures

def is_action(action):
	"a check to see if the instance _action_ is a subclass of aioopenflow.Action.Action"
	try:
		return issubclass(msg.__class__, Message)
	except AttributeError:
		return False

#baseclass
class Action:
	type = None
	raw_payload = b""
	def __init__(self, version=None):
		if version is not None:
			self.version = version#should be set by container
	def unpack(self, data):
		assert self.version
		
		typenum = int.from_bytes(data[0:2], byteorder="big")
		length  = int.from_bytes(data[2:4], byteorder="big")
		self.raw_payload = data[4:length]
		
		if len(data) != length:
			logger.warning(f"{self.__class__.__name__}.unpack: length mismatch with len(data): {length} vs {len(data)}")
		
		self.type = aioopenflow.constants.getActionType(self.version, typenum)
		
		return self
	def pack(self):
		assert self.version
		assert type(self.type) is aioopenflow.types.ActionType
		
		payload = bytes(self.raw_payload)
		out = (
			self.type.for_version(self.version).to_bytes(2, byteorder='big'),
			(len(payload)+4).to_bytes(2, byteorder='big'),
			payload,
		)
		
		return b"".join(out)

#subclasses
class ActionOutput(Action):
	type = aioopenflow.constants.AT_Output
	port = 0
	max_len = 0xffe5#Max length to send to controller.
	def __init__(self, port, max_len = 0xffe5):
		self.port = port
		self.max_len = max_len
	def raw_payload():
		def fget(self):
			assert self.version == aioopenflow.constants.openflow10#todo
			assert type(self.port) is int or type(self.port) is aioopenflow.types.NamedInt, self.port
			assert type(self.max_len) is int, self.max_len
			
			out = (
				(self.port&0xFFFF).to_bytes(2, byteorder='big'),
				self.max_len      .to_bytes(2, byteorder='big'),
			)
			
			return b"".join(out)
		def fset(self, value):
			assert self.version == aioopenflow.constants.openflow10#todo
			
			self.port    = int.from_bytes(value[0:2], byteorder='big')
			self.max_len = int.from_bytes(value[2:4], byteorder='big')
			
		return locals()
	raw_payload = property(**raw_payload())

class ActionSetVLANVID(Action):
	type = aioopenflow.constants.AT_SetVLANVID

class ActionSetVLANPCP(Action):
	type = aioopenflow.constants.AT_SetVLANPCP

class ActionStripVLAN(Action):
	type = aioopenflow.constants.AT_StripVLAN

class ActionSetDLSrc(Action):
	type = aioopenflow.constants.AT_SetDLSrc

class ActionSetDLDst(Action):
	type = aioopenflow.constants.AT_SetDLDst

class ActionSetNWSrc(Action):
	type = aioopenflow.constants.AT_SetNWSrc

class ActionSetNWDst(Action):
	type = aioopenflow.constants.AT_SetNWDst

class ActionSetNWTos(Action):
	type = aioopenflow.constants.AT_SetNWTos

class ActionSetNWECN(Action):
	type = aioopenflow.constants.AT_SetNWECN

class ActionSetTPSrc(Action):
	type = aioopenflow.constants.AT_SetTPSrc

class ActionSetTPDst(Action):
	type = aioopenflow.constants.AT_SetTPDst

class ActionEnqueue(Action):
	type = aioopenflow.constants.AT_Enqueue

class ActionCopyTTLOut(Action):
	type = aioopenflow.constants.AT_CopyTTLOut

class ActionCopyTTLIn(Action):
	type = aioopenflow.constants.AT_CopyTTLIn

class ActionSetMPLSLabel(Action):
	type = aioopenflow.constants.AT_SetMPLSLabel

class ActionSetMPLSTC(Action):
	type = aioopenflow.constants.AT_SetMPLSTC

class ActionSetMPLSTTL(Action):
	type = aioopenflow.constants.AT_SetMPLSTTL

class ActionDecMPLSTTL(Action):
	type = aioopenflow.constants.AT_DecMPLSTTL

class ActionPushVLAN(Action):
	type = aioopenflow.constants.AT_PushVLAN

class ActionPopVLAN(Action):
	type = aioopenflow.constants.AT_PopVLAN

class ActionPushMPLS(Action):
	type = aioopenflow.constants.AT_PushMPLS

class ActionPopMPLS(Action):
	type = aioopenflow.constants.AT_PopMPLS
	
class ActionSetQueue(Action):
	type = aioopenflow.constants.AT_SetQueue

class ActionGroup(Action):
	type = aioopenflow.constants.AT_Group
	
class ActionSetNWTTL(Action):
	type = aioopenflow.constants.AT_SetNWTTL
	
class ActionDecNWTTL(Action):
	type = aioopenflow.constants.AT_DecNWTTL
	
class ActionSetField(Action):
	type = aioopenflow.constants.AT_SetField
	
class ActionPushPBB(Action):
	type = aioopenflow.constants.AT_PushPBB

class ActionPopPBB(Action):
	type = aioopenflow.constants.AT_PopPBB

class ActionExperimenter(Action):
	type = aioopenflow.constants.AT_Experimenter

class ActionVendor(Action):
	type = aioopenflow.constants.AT_Vendor



ActionType_to_Action = {
	aioopenflow.constants.AT_Output       : ActionOutput,
	aioopenflow.constants.AT_SetVLANVID   : ActionSetVLANVID,
	aioopenflow.constants.AT_SetVLANPCP   : ActionSetVLANPCP,
	aioopenflow.constants.AT_StripVLAN    : ActionStripVLAN,
	aioopenflow.constants.AT_SetDLSrc     : ActionSetDLSrc,
	aioopenflow.constants.AT_SetDLDst     : ActionSetDLDst,
	aioopenflow.constants.AT_SetNWSrc     : ActionSetNWSrc,
	aioopenflow.constants.AT_SetNWDst     : ActionSetNWDst,
	aioopenflow.constants.AT_SetNWTos     : ActionSetNWTos,
	aioopenflow.constants.AT_SetNWECN     : ActionSetNWECN,
	aioopenflow.constants.AT_SetTPSrc     : ActionSetTPSrc,
	aioopenflow.constants.AT_SetTPDst     : ActionSetTPDst,
	aioopenflow.constants.AT_Enqueue      : ActionEnqueue,
	aioopenflow.constants.AT_CopyTTLOut   : ActionCopyTTLOut,
	aioopenflow.constants.AT_CopyTTLIn    : ActionCopyTTLIn,
	aioopenflow.constants.AT_SetMPLSLabel : ActionSetMPLSLabel,
	aioopenflow.constants.AT_SetMPLSTC    : ActionSetMPLSTC,
	aioopenflow.constants.AT_SetMPLSTTL   : ActionSetMPLSTTL,
	aioopenflow.constants.AT_DecMPLSTTL   : ActionDecMPLSTTL,
	aioopenflow.constants.AT_PushVLAN     : ActionPushVLAN,
	aioopenflow.constants.AT_PopVLAN      : ActionPopVLAN,
	aioopenflow.constants.AT_PushMPLS     : ActionPushMPLS,
	aioopenflow.constants.AT_PopMPLS      : ActionPopMPLS,
	aioopenflow.constants.AT_SetQueue     : ActionSetQueue,
	aioopenflow.constants.AT_Group        : ActionGroup,
	aioopenflow.constants.AT_SetNWTTL     : ActionSetNWTTL,
	aioopenflow.constants.AT_DecNWTTL     : ActionDecNWTTL,
	aioopenflow.constants.AT_SetField     : ActionSetField,
	aioopenflow.constants.AT_PushPBB      : ActionPushPBB,
	aioopenflow.constants.AT_PopPBB       : ActionPopPBB,
	aioopenflow.constants.AT_Experimenter : ActionExperimenter,
	aioopenflow.constants.AT_Vendor       : ActionVendor,
}
