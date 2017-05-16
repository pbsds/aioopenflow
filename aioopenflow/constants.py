from aioopenflow.types import MessageType, ErrorType, ErrorCode
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

def getMessageType(version, typenum):
	for key, messagetype in globals().items():
		if key[:3] == "MT_":
			if messagetype.for_version(version, silence=True) == typenum:
				return messagetype
	raise Exception(f"No defined MessageType for version {version} with type {typenum}")



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
#CA[openflow10].[0x004] = "CA_PORT_STATS"



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
PORT_Max        = 0xFFFFFF00
PORT_InPort     = 0xFFFFFFF8
PORT_Table      = 0xFFFFFFF9
PORT_Normal     = 0xFFFFFFFA
PORT_Flood      = 0xFFFFFFFB
PORT_All        = 0xFFFFFFFC
PORT_Controller = 0xFFFFFFFD
PORT_Local      = 0xFFFFFFFE
PORT_Any        = 0xFFFFFFFF#of v1.1 and 1v2
PORT_None       = 0xFFFFFFFF#of v1.0
PORTS = (PORT_Max, PORT_InPort, PORT_Table, PORT_Normal, PORT_Flood, PORT_All, PORT_Controller, PORT_Local, PORT_Any, PORT_None)





		








