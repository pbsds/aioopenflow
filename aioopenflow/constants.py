from aioopenflow.types import MessageType, ErrorType, ErrorCode, NamedInt, ActionType
#http://flowgrammable.org/sdn/openflow/message-layer/#tab_ofp_1_4

#openflow versions:
openflow10 = 1
openflow11 = 2
openflow12 = 3
openflow13 = 4
openflow14 = 5



#openflow message types:
MT_Hello             = MessageType(( 0,  0,  0,  0,  0, "Hello"))#one for each version
MT_Error             = MessageType(( 1,  1,  1,  1,  1, "Error"))
MT_EchoReq           = MessageType(( 2,  2,  2,  2,  2, "EchoReq"))
MT_EchoRes           = MessageType(( 3,  3,  3,  3,  3, "EchoRes"))
MT_Vendor            = MessageType(( 4, -1, -1, -1, -1, "Vendor"))
MT_Experimenter      = MessageType((-1,  4,  4,  4,  4, "Experimenter"))
MT_FeatureReq        = MessageType(( 5,  5,  5,  5,  5, "FeatureReq"))
MT_FeatureRes        = MessageType(( 6,  6,  6,  6,  6, "FeatureRes"))
MT_GetConfigReq      = MessageType(( 7,  7,  7,  7,  7, "GetConfigReq"))
MT_GetConfigRes      = MessageType(( 8,  8,  8,  8,  8, "GetConfigRes"))
MT_SetConfig         = MessageType(( 9,  9,  9,  9,  9, "SetConfig"))
MT_PacketIn          = MessageType((10, 10, 10, 10, 10, "PacketIn"))
MT_FlowRemoved       = MessageType((11, 11, 11, 11, 11, "FlowRemoved"))
MT_PortStatus        = MessageType((12, 12, 12, 12, 12, "PortStatus"))
MT_PacketOut         = MessageType((13, 13, 13, 13, 13, "PacketOut"))
MT_FlowMod           = MessageType((14, 14, 14, 14, 14, "FlowMod"))
MT_PortMod           = MessageType((15, 16, 16, 16, 16, "PortMod"))
MT_GroupMod          = MessageType((-1, 15, 15, 15, 15, "GroupMod"))
MT_TableMod          = MessageType((-1, 17, 17, 17, 17, "TableMod"))
MT_StatsReq          = MessageType((16, 18, 18, -1, -1, "StatsReq"))
MT_StatsRes          = MessageType((17, 19, 19, -1, -1, "StatsRes"))
MT_BarrierReq        = MessageType((18, 20, 20, 20, 20, "BarrierReq"))
MT_BarrierRes        = MessageType((19, 21, 21, 21, 21, "BarrierRes"))
MT_MultipartReq      = MessageType((-1, -1, -1, 18, 18, "MultipartReq"))
MT_MultipartRes      = MessageType((-1, -1, -1, 19, 19, "MultipartRes"))
MT_QueueGetConfigReq = MessageType((20, 22, 22, 22, -1, "QueueGetConfigReq"))
MT_QueueGetConfigRes = MessageType((21, 23, 23, 23, -1, "QueueGetConfigRes"))
MT_RoleReq           = MessageType((-1, -1, 24, 24, 24, "RoleReq"))
MT_RoleRes           = MessageType((-1, -1, 25, 25, 25, "RoleRes"))
MT_GetAsyncReq       = MessageType((-1, -1, -1, 26, 26, "GetAsyncReq"))
MT_GetAsyncRes       = MessageType((-1, -1, -1, 27, 27, "GetAsyncRes"))
MT_SetAsync          = MessageType((-1, -1, -1, 28, 28, "SetAsync"))
MT_MeterMod          = MessageType((-1, -1, -1, 29, 29, "MeterMod"))
MT_TableStatus       = MessageType((-1, -1, -1, -1, 31, "TableStatus"))
MT_RoleStatus        = MessageType((-1, -1, -1, -1, 30, "RoleStatus"))
MT_RequestForward    = MessageType((-1, -1, -1, -1, 32, "RequestForward"))
MT_BundleControl     = MessageType((-1, -1, -1, -1, 33, "BundleControl"))
MT_BundleAddMessage  = MessageType((-1, -1, -1, -1, 34, "BundleAddMessage"))
MTs = tuple(messagetype for key, messagetype in locals().items() if key[:3] == "MT_")

def getMessageType(version, typenum):
	for messagetype in MTs:
		if messagetype.for_version(version, silence=True) == typenum:
			return messagetype
	raise Exception(f"No defined MessageType for version {version} with type {typenum}")



#openflow action types
AT_Output       = ActionType((0x0000, 0x0000, 0x0000, 0x0000,     -1, "Output"))
AT_SetVLANVID   = ActionType((0x0001, 0x0001,     -1,     -1,     -1, "SetVLANVID"))
AT_SetVLANPCP   = ActionType((0x0002, 0x0002,     -1,     -1,     -1, "SetVLANPCP"))
AT_StripVLAN    = ActionType((0x0003,     -1,     -1,     -1,     -1, "StripVLAN"))
AT_SetDLSrc     = ActionType((0x0004, 0x0003,     -1,     -1,     -1, "SetDLSrc"))
AT_SetDLDst     = ActionType((0x0005, 0x0004,     -1,     -1,     -1, "SetDLDst"))
AT_SetNWSrc     = ActionType((0x0006, 0x0005,     -1,     -1,     -1, "SetNWSrc"))
AT_SetNWDst     = ActionType((0x0007, 0x0006,     -1,     -1,     -1, "SetNWDst"))
AT_SetNWTos     = ActionType((0x0008, 0x0007,     -1,     -1,     -1, "SetNWTos"))
AT_SetNWECN     = ActionType((    -1, 0x0008,     -1,     -1,     -1, "SetNWECN"))
AT_SetTPSrc     = ActionType((0x0009, 0x0009,     -1,     -1,     -1, "SetTPSrc"))
AT_SetTPDst     = ActionType((0x000a, 0x000a,     -1,     -1,     -1, "SetTPDst"))
AT_Enqueue      = ActionType((0x000b,     -1,     -1,     -1,     -1, "Enqueue"))
AT_CopyTTLOut   = ActionType((    -1, 0x000b, 0x000b, 0x000b,     -1, "CopyTTLOut"))
AT_CopyTTLIn    = ActionType((    -1, 0x000c, 0x000c, 0x000c,     -1, "CopyTTLIn"))
AT_SetMPLSLabel = ActionType((    -1, 0x000d,     -1,     -1,     -1, "SetMPLSLabel"))
AT_SetMPLSTC    = ActionType((    -1, 0x000e,     -1,     -1,     -1, "SetMPLSTC"))
AT_SetMPLSTTL   = ActionType((    -1, 0x000f, 0x000f, 0x000f,     -1, "SetMPLSTTL"))
AT_DecMPLSTTL   = ActionType((    -1, 0x0010, 0x0010, 0x0010,     -1, "DecMPLSTTL"))
AT_PushVLAN     = ActionType((    -1, 0x0011, 0x0011, 0x0011,     -1, "PushVLAN"))
AT_PopVLAN      = ActionType((    -1, 0x0012, 0x0012, 0x0012,     -1, "PopVLAN"))
AT_PushMPLS     = ActionType((    -1, 0x0013, 0x0013, 0x0013,     -1, "PushMPLS"))
AT_PopMPLS      = ActionType((    -1, 0x0014, 0x0014, 0x0014,     -1, "PopMPLS"))
AT_SetQueue     = ActionType((    -1, 0x0015, 0x0015, 0x0015,     -1, "SetQueue"))
AT_Group        = ActionType((    -1, 0x0016, 0x0016, 0x0016,     -1, "Group"))
AT_SetNWTTL     = ActionType((    -1, 0x0017, 0x0017, 0x0017,     -1, "SetNWTTL"))
AT_DecNWTTL     = ActionType((    -1, 0x0018, 0x0018, 0x0018,     -1, "DecNWTTL"))
AT_SetField     = ActionType((    -1,     -1, 0x0019, 0x0019,     -1, "SetField"))
AT_PushPBB      = ActionType((    -1,     -1,     -1, 0x001a,     -1, "PushPBB"))
AT_PopPBB       = ActionType((    -1,     -1,     -1, 0x001b,     -1, "PopPBB"))
AT_Experimenter = ActionType((    -1, 0xffff, 0xffff, 0xffff,     -1, "Experimenter"))
AT_Vendor       = ActionType((0xffff,     -1,     -1,     -1,     -1, "Vendor"))
ATs = tuple(actiontype for key, actiontype in locals().items() if key[:3] == "AT_")

def getActionType(version, typenum):
	for actiontype in ATs:
		if actiontype.for_version(version, silence=True) == typenum:
			return actiontype
	raise Exception(f"No defined ActionType for version {version} with type {typenum}")



#Error codes:
ER_HelloFailed = ErrorType(0x0000, 0x0000, 0x0000, 0x0000, 0x0000, "HelloFailed")
ER_HelloFailed.Incompatible = ErrorCode(0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
ER_HelloFailed.EPerm        = ErrorCode(0x0001, 0x0001, 0x0001, 0x0001, 0x0001)#permissions error

ER_BadRequest = ErrorType(0x0001, None, None, None, None, "BadRequest")
ER_BadRequest.BadVersion    = ErrorCode(0x0000, None, None, None, None)
ER_BadRequest.BadType       = ErrorCode(0x0001, None, None, None, None)
ER_BadRequest.BadStat       = ErrorCode(0x0002, None, None, None, None)
ER_BadRequest.BadVendor     = ErrorCode(0x0003, None, None, None, None)
ER_BadRequest.BadSubtype    = ErrorCode(0x0004, None, None, None, None)
ER_BadRequest.EPerm         = ErrorCode(0x0005, None, None, None, None)#permissions error
ER_BadRequest.BadLength     = ErrorCode(0x0006, None, None, None, None)
ER_BadRequest.BufferEmpty   = ErrorCode(0x0007, None, None, None, None)
ER_BadRequest.BufferUnknown = ErrorCode(0x0008, None, None, None, None)

ER_BadAction = ErrorType(0x0002, None, None, None, None, "BadAction")
ER_BadAction.BadType       = ErrorCode(0x0000, None, None, None, None)
ER_BadAction.BadLength     = ErrorCode(0x0001, None, None, None, None)
ER_BadAction.BadVendor     = ErrorCode(0x0002, None, None, None, None)
ER_BadAction.BadVendorType = ErrorCode(0x0003, None, None, None, None)
ER_BadAction.BadOutPort    = ErrorCode(0x0004, None, None, None, None)
ER_BadAction.BadArgument   = ErrorCode(0x0005, None, None, None, None)
ER_BadAction.EPerm         = ErrorCode(0x0006, None, None, None, None)#permissions error
ER_BadAction.TooMany       = ErrorCode(0x0007, None, None, None, None)
ER_BadAction.BadQueue      = ErrorCode(0x0008, None, None, None, None)

ER_FlowModFailed = ErrorType(0x0003, None, None, None, None, "FlowModFailed")
ER_FlowModFailed.AllTablesFull   = ErrorCode(0x0000, None, None, None, None)
ER_FlowModFailed.Overlap         = ErrorCode(0x0002, None, None, None, None)
ER_FlowModFailed.EPerm           = ErrorCode(0x0003, None, None, None, None)#permissions error
ER_FlowModFailed.BadEmergTimeout = ErrorCode(0x0004, None, None, None, None)
ER_FlowModFailed.BadCommand      = ErrorCode(0x0005, None, None, None, None)
ER_FlowModFailed.Unsupported     = ErrorCode(0x0006, None, None, None, None)

ER_PortModFailed = ErrorType(0x0004, None, None, None, None, "PortModFailed")
ER_PortModFailed.BadPort   = ErrorCode(0x0000, None, None, None, None)
ER_PortModFailed.BadHwAddr = ErrorCode(0x0001, None, None, None, None)

ER_QueueOpFailed = ErrorType(0x0005, None, None, None, None, "QueueOpFailed")
ER_QueueOpFailed.BadPort  = ErrorCode(0x0000, None, None, None, None)
ER_QueueOpFailed.BadQueue = ErrorCode(0x0001, None, None, None, None)
ER_QueueOpFailed.EPerm    = ErrorCode(0x0002, None, None, None, None)#permissions error

#ER_ = ErrorType(0x0001, None, None, None, None, "")
#ER_. = ErrorCode(None, None, None, None, None)

def getErrorCode(version, type, code):
	for key, errortype in globals().items():
		if key[:3] == "ER_":
			for child in dir(errortype):
				if child[0] != "_":
					errorcode = getattr(errortype, child)
					if errorcode.for_version(version) == (type, code):
						return errorcode
	raise Exception(f"No defined ErrorCode for version {version} with value ({type}, {code})")



#capabilities:
CA = (None,
	{#openflow10:
		0x00000001 : "FLOW_STATS",
		0x00000002 : "TABLE_STATS",
		0x00000004 : "PORT_STATS",
		0x00000008 : "STP",
		0x00000010 : "RESERVED",
		0x00000020 : "IP_REASM",
		0x00000040 : "QUEUE_STATS",
		0x00000080 : "ARP_MATCH_IP",
	},{#openflow11:
		0x00000001 : "FLOW_STATS",
		0x00000002 : "TABLE_STATS",
		0x00000004 : "PORT_STATS",
		0x00000008 : "GROUP_STATS",
		0x00000020 : "IP_REASM",
		0x00000040 : "QUEUE_STATS",
		0x00000080 : "ARP_MATCH_IP",
	},{#openflow12:
		0x00000001 : "FLOW_STATS",
		0x00000002 : "TABLE_STATS",
		0x00000004 : "PORT_STATS",
		0x00000008 : "GROUP_STATS",
		0x00000020 : "IP_REASM",
		0x00000040 : "QUEUE_STATS",
		0x00000100 : "PORT_BLOCKED",
	},{#openflow13:
		0x00000001 : "FLOW_STATS",
		0x00000002 : "TABLE_STATS",
		0x00000004 : "PORT_STATS",
		0x00000008 : "GROUP_STATS",
		0x00000020 : "IP_REASM",
		0x00000040 : "QUEUE_STATS",
		0x00000100 : "PORT_BLOCKED",
	},{#openflow14:
		0x00000001 : "FLOW_STATS",
		0x00000002 : "TABLE_STATS",
		0x00000004 : "PORT_STATS",
		0x00000008 : "GROUP_STATS",
		0x00000020 : "IP_REASM",
		0x00000040 : "QUEUE_STATS",
		0x00000100 : "PORT_BLOCKED",
	}
)
#use:
#CA[openflow10].[0x004] == "CA_PORT_STATS"



#actions
#these are only used in openflow v1.0
ACTIONS = {
	0x00000001 : "OUTPUT",
	0x00000002 : "SET_VLAN_VID",
	0x00000004 : "SET_VLAN_PCP",
	0x00000008 : "STRIP_VLAN",
	0x00000010 : "SET_DL_SRC",
	0x00000020 : "SET_DL_DST",
	0x00000040 : "SET_NW_SRC",
	0x00000080 : "SET_NW_DST",
	0x00000100 : "SET_NW_TOS",
	0x00000200 : "SET_TP_SRC",
	0x00000400 : "SET_TP_DST",
	0x00000800 : "ENQUEUE",
}



#switch ports:
PORT_ID_Max        = NamedInt(0xFFFFFF00, "Max")
PORT_ID_InPort     = NamedInt(0xFFFFFFF8, "InPort")
PORT_ID_Table      = NamedInt(0xFFFFFFF9, "Table")
PORT_ID_Normal     = NamedInt(0xFFFFFFFA, "Normal")
PORT_ID_Flood      = NamedInt(0xFFFFFFFB, "Flood")
PORT_ID_All        = NamedInt(0xFFFFFFFC, "All")
PORT_ID_Controller = NamedInt(0xFFFFFFFD, "Controller")
PORT_ID_Local      = NamedInt(0xFFFFFFFE, "Local")
PORT_ID_Any        = NamedInt(0xFFFFFFFF, "Any") #of v1.1 and 1v2
PORT_ID_None       = NamedInt(0xFFFFFFFF, "None")#of v1.0
PORT_IDS = (PORT_ID_Max, PORT_ID_InPort, PORT_ID_Table, PORT_ID_Normal, PORT_ID_Flood, PORT_ID_All, PORT_ID_Controller, PORT_ID_Local, PORT_ID_Any, PORT_ID_None)

PORT_CONFIG = {
	0x00000001 : "PortDown",
	0x00000002 : "NoSTP",#only used in openflow v1.0
	0x00000004 : "NoRecv",
	0x00000008 : "NoRecvSTP",#only used in openflow v1.0
	0x00000010 : "NoFlood",#only used in openflow v1.0
	0x00000020 : "NoFwd",
	0x00000040 : "NoPacketIn",
}

PORT_STATES = (None,
	{#openflow v1.0
		0x00000000 : "STPListen",
		0x00000001 : "LinkDown",
		0x00000002 : "STPLearn",
		0x00000004 : "STPForward",
		0x00000008 : "STPBlock",
		0x00000010 : "STPMask",
	}, {#openflow v1.1
		0x00000001 : "LinkDown",
		0x00000002 : "Blocked",
		0x00000004 : "Live",
	}, {#openflow v1.2
		0x00000001 : "LinkDown",
		0x00000002 : "Blocked",
		0x00000004 : "Live",
	}, {#openflow v1.3
		0x00000001 : "LinkDown",
		0x00000002 : "Blocked",
		0x00000004 : "Live",
	}
)
#use:
#PORT_STATES[openflow10].[0x004] == "NoRecv"

PORT_FEATURE = {
	0x00000001 : "10MB_HD",
	0x00000002 : "10MB_FD",
	0x00000004 : "100MB_HD",
	0x00000008 : "100MB_FD",
	0x00000010 : "1GB_HD",
	0x00000020 : "1GB_FD",
	0x00000040 : "10GB_FD",
	0x00000080 : "40GB_FD", #not used in openflow 1.0
	0x00000100 : "100GB_FD",#not used in openflow 1.0
	0x00000200 : "1TB_FD",  #not used in openflow 1.0
	0x00000400 : "Other",   #not used in openflow 1.0
	0x00000800 : "Copper",
	0x00001000 : "Fiber",
	0x00002000 : "AutoNeg",
	0x00004000 : "Pause",
	0x00008000 : "PauseAsym",
}




