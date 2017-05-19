import aioopenflow.constants
import copy

class Match:
	version = None
	oxms = None
	def __init__(self):
		oxms = []
	def add_OXM(self, oxm):
		if oxm._dependencies:
			for d in oxm._dependencies:
				if d not in oxms:
					self.oxms.append(copy.copy(d))
		for i, o in enumerate(self.oxms):
			if o.classnum == oxm.classnum:
				self.oxms[i] = oxm
				break
		else:
			self.oxms.append(oxm)
	def pack(self):
		assert self.version == aioopenflow.constants.openflow10
		
		if self.version == aioopenflow.constants.openflow10:
			return self._pack10()
		elif self.version == aioopenflow.constants.openflow11:
			return self._pack11()
		else:#openflow 1.2 and above
			pass#todo: ez?
		
	def _pack10(self):
		wildcards = 0
		in_port   = 0
		dl_src    = 0
		dl_dst    = 0
		dl_vlan   = 0
		dl_pcp    = 0
		dl_type   = 0
		nw_tos    = 0
		nw_proto  = 0
		nw_src    = 0
		nw_dst    = 0
		tp_src    = 0
		tp_dst    = 0
		
		for oxm in self.oxms:
			if oxm.fieldvalue == OXM_in_port.fieldvalue:
				in_port = OXM.data
				wildcards |= 0x00000001
			elif oxm.fieldvalue == OXM_eth_src.fieldvalue:
				dl_src = OXM.data
				wildcards |= 0x00000004
			elif oxm.fieldvalue == OXM_eth_dst.fieldvalue:
				dl_dst = OXM.data
				wildcards |= 0x00000008
			elif oxm.fieldvalue == OXM_vlan_vid.fieldvalue:
				dl_vlan = OXM.data
				wildcards |= 0x00000002
			elif oxm.fieldvalue == OXM_vlan_pcp.fieldvalue:
				dl_pcp = OXM.data
				wildcards |= 0x00100000
			elif oxm.fieldvalue == OXM_eth_type.fieldvalue:
				dl_type = OXM.data
				wildcards |= 0x00000010
			elif oxm.fieldvalue == OXM_ip_dscp.fieldvalue:
				nw_tos = OXM.data
				wildcards |= 0x00200000
			elif oxm.fieldvalue == OXM_ip_proto.fieldvalue:
				nw_proto = OXM.data
				wildcards |= 0x00000020
			elif oxm.fieldvalue == OXM_arp_op.fieldvalue:
				nw_proto = OXM.data & 0xFF
				wildcards |= 0x00000020
			elif oxm.fieldvalue == OXM_ipv4_src.fieldvalue:
				nw_src = OXM.data
				if OXM.hasmask:
					VLSM = bin(int.from_bytes(OXM.payload_raw[4:], byteorder="big")).count("1")
					wildcards |= (32-VLSM) << 8
			elif oxm.fieldvalue == OXM_ipv4_dst.fieldvalue:
				nw_dst = OXM.data
				if OXM.hasmask:
					VLSM = bin(int.from_bytes(OXM.payload_raw[4:], byteorder="big")).count("1")
					wildcards |= (32-VLSM) << 14
			elif oxm.fieldvalue == OXM_tcp_src.fieldvalue:
				tp_src = OXM.data
				wildcards |= 0x00000040
			elif oxm.fieldvalue == OXM_tcp_dst.fieldvalue:
				tp_dst = OXM.data
				wildcards |= 0x00000080
		
		out = (
			wildcards.to_bytes(4, byteorder='big'),
			in_port  .to_bytes(2, byteorder='big'),
			dl_src   .to_bytes(6, byteorder='big'),
			dl_dst   .to_bytes(6, byteorder='big'),
			dl_vlan  .to_bytes(2, byteorder='big'),
			dl_pcp   .to_bytes(1, byteorder='big'),
			"\0",
			dl_type  .to_bytes(2, byteorder='big'),
			nw_tos   .to_bytes(1, byteorder='big'),
			nw_proto .to_bytes(1, byteorder='big'),
			"\0\0",
			nw_src   .to_bytes(4, byteorder='big'),
			nw_dst   .to_bytes(4, byteorder='big'),
			tp_src   .to_bytes(2, byteorder='big'),
			tp_dst   .to_bytes(2, byteorder='big'),
		)
		return b"".join(out)
	def _pack11(self):
		pass#todo
	def unpack():
		raise NotImplementedError()

def from_ip_packet(packet):
	if type(packet) is bytes:
		packet = Packet(packet)
	match = Match()
	

#base
class OXM:
	classnum      = 0x8000#OpenFlowBasic
	fieldlength   = None#in bits
	fieldvalue    = None#int
	_dependencies = None#(OXM1(), OXM2(), ...)
	hasmask       = False
	
	payload_raw = b"\0"
	def __init__(self, data = None, payload_raw=None, hasmask=None):
		fieldlength = self.fieldlength
		if self.hasmask: fieldlength *= 2
		self.payload_raw = "\0" * int(fieldlength/8 + 0.5)
		
		if data is not None:        self.data = data
		if payload_raw is not None: self.payload_raw = payload_raw
		if hasmask is not None:	    self.hasmask = hasmask
	def __eq__(self, oxm):
		out = (
			self.classnum    == oxm.classnum,
			self.fieldlength == oxm.fieldlength,
			self.fieldvalue  == oxm.fieldvalue,
			self.hasmask     == oxm.hasmask,
			self.payload_raw == oxm.payload_raw,
		)
		return False not in out
	def __hash__(self):
		out = (
			self.classnum,
			self.fieldlength,
			self.fieldvalue,
			self.hasmask,
			self.payload_raw,
		)
		return hash(sum(hash(i) for i in out))
	def pack():
		payload_raw = self.payload_raw
		assert type(payload_raw) is bytes
		assert len(payload_raw) >= 1
		
		fieldlength = self.fieldlength
		if self.hasmask: fieldlength *= 2
		fieldlength = int(fieldlength/8 + 0.5)
		
		fieldvalue = ((self.fieldvalue & 0x7F) << 1 ) | bool(self.hasmask)
		
		out = (
			self.classnum   .to_bytes(2, byteorder='big'),
			fieldvalue      .to_bytes(1, byteorder='big'),
			fieldlength.to_bytes(1, byteorder='big'),
			payload_raw,
		)
		return b"".join(out)
	def unpack():
		raise NotImplementedError()
	def data():
		def fget(self):
			return int.from_bytes(self.payload_raw, byteorder="big")
		def fset(self, value):
			fieldlength = self.fieldlength
			if self.hasmask: fieldlength *= 2
			fieldlength =  int(fieldlength/8 + 0.5)
			
			self.payload_raw = value.to_bytes(fieldlength, byteorder="big")
		return locals()
	data = property(**data())

#subclasses
class OXM_in_port(OXM):#Switch input port
	fieldlength   = 32
	fieldvalue    = 0x00
	hasmask       = 0

class OXM_in_phy_port(OXM):#Switch physical input port
	fieldlength   = 32
	fieldvalue    = 0x01
	hasmask       = 0
	_dependencies = (OXM_in_port)

class OXM_metadata(OXM):#Metadata passed between tables
	fieldlength   = 64
	fieldvalue    = 0x02
	hasmask       = 0

class OXM_eth_dst(OXM):#Ethernet destination address
	fieldlength   = 48
	fieldvalue    = 0x03
	hasmask       = 0

class OXM_eth_src(OXM):#Ethernet source address
	fieldlength   = 48
	fieldvalue    = 0x04
	hasmask       = 0

class OXM_eth_type(OXM):#Ethernet frame type
	fieldlength   = 16
	fieldvalue    = 0x05
	hasmask       = 0

class OXM_vlan_vid(OXM):#VLAN id
	fieldlength   = 13
	fieldvalue    = 0x06
	hasmask       = 0

class OXM_vlan_pcp(OXM):#VLAN priority
	fieldlength   = 3
	fieldvalue    = 0x07
	hasmask       = 0
	_dependencies = (OXM_vlan_vid)

class OXM_ip_dscp(OXM):#IP DSCP (6 bits in ToS field)
	fieldlength   = 6
	fieldvalue    = 0x08
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0800), OXM_eth_type(0x86dd))

class OXM_ip_ecn(OXM):#IP ECN (2 bits in ToS field)
	fieldlength   = 2
	fieldvalue    = 0x09
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0800), OXM_eth_type(0x86dd))

class OXM_ip_proto(OXM):#IP protocol
	fieldlength   = 8
	fieldvalue    = 0x0a
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0800), OXM_eth_type(0x86dd))

class OXM_ipv4_src(OXM):#IPv4 source address
	fieldlength   = 32
	fieldvalue    = 0x0b
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0800))

class OXM_ipv4_dst(OXM):#IPv4 destination address
	fieldlength   = 32
	fieldvalue    = 0x0c
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0800))

class OXM_tcp_src(OXM):#TCP source port
	fieldlength   = 16
	fieldvalue    = 0x0d
	hasmask       = 0
	_dependencies = (OXM_ip_proto(6))

class OXM_tcp_dst(OXM):#TCP destination port
	fieldlength   = 16
	fieldvalue    = 0x0e
	hasmask       = 0
	_dependencies = (OXM_ip_proto(6))

class OXM_udp_src(OXM):#UDP source port
	fieldlength   = 16
	fieldvalue    = 0x0f
	hasmask       = 0
	_dependencies = (OXM_ip_proto(17))

class OXM_udp_dst(OXM):#UDP destination port
	fieldlength   = 16
	fieldvalue    = 0x10
	hasmask       = 0
	_dependencies = (OXM_ip_proto(17))

class OXM_sctp_src(OXM):#SCTP source port
	fieldlength   = 16
	fieldvalue    = 0x11
	hasmask       = 0
	_dependencies = (OXM_ip_proto(132))

class OXM_sctp_dst(OXM):#SCTP destination port
	fieldlength   = 16
	fieldvalue    = 0x12
	hasmask       = 0
	_dependencies = (OXM_ip_proto(132))

class OXM_icmpv4_type(OXM):#ICMP type
	fieldlength   = 8
	fieldvalue    = 0x13
	hasmask       = 0
	_dependencies = (OXM_ip_proto(1))

class OXM_icmpv4_code(OXM):#ICMP code
	fieldlength   = 8
	fieldvalue    = 0x14
	hasmask       = 0
	_dependencies = (OXM_ip_proto(1))

class OXM_arp_op(OXM):#ARP opcode
	fieldlength   = 16
	fieldvalue    = 0x15
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0806))

class OXM_arp_spa(OXM):#ARP source IPv4 address
	fieldlength   = 32
	fieldvalue    = 0x16
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0806))

class OXM_arp_tpa(OXM):#ARP target IPv4 address
	fieldlength   = 32
	fieldvalue    = 0x17
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0806))

class OXM_arp_sha(OXM):#ARP source hardware address
	fieldlength   = 48
	fieldvalue    = 0x18
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0806))

class OXM_arp_tha(OXM):#ARP target hardware address
	fieldlength   = 48
	fieldvalue    = 0x19
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x0806))

class OXM_ipv6_src(OXM):#IPv6 source address
	fieldlength   = 128
	fieldvalue    = 0x1a
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x86dd))

class OXM_ipv6_dst(OXM):#IPv6 destination address
	fieldlength   = 128
	fieldvalue    = 0x1b
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x86dd))

class OXM_ipv6_flabel(OXM):#IPv6 Flow Labe
	fieldlength   = 20
	fieldvalue    = 0x1c
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x86dd))

class OXM_icmpv6_type(OXM):#ICMPv6 type
	fieldlength   = 8
	fieldvalue    = 0x1d
	hasmask       = 0
	_dependencies = (OXM_ip_proto(58))

class OXM_icmpv6_code(OXM):#ICMPv6 code
	fieldlength   = 8
	fieldvalue    = 0x1e
	hasmask       = 0
	_dependencies = (OXM_ip_proto(58))

class OXM_ipv6_nd_target(OXM):#Target address for ND
	fieldlength   = 128
	fieldvalue    = 0x1f
	hasmask       = 0
	_dependencies = (OXM_icmpv6_type(135), OXM_icmpv6_type(136))

class OXM_ipv6_nd_sll(OXM):#Source link-layer for ND
	fieldlength   = 48
	fieldvalue    = 0x20
	hasmask       = 0
	_dependencies = (OXM_icmpv6_type(135))

class OXM_ipv6_nd_tll(OXM):#Target link-layer for ND
	fieldlength   = 48
	fieldvalue    = 0x21
	hasmask       = 0
	_dependencies = (OXM_icmpv6_type(136))

class OXM_mpls_label(OXM):#MPLS label
	fieldlength   = 20
	fieldvalue    = 0x22
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x8847), OXM_eth_type(0x8848))

class OXM_mpls_tc(OXM):#MPLS TC
	fieldlength   = 3
	fieldvalue    = 0x23
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x8847), OXM_eth_type(0x8848))

class OXM_mpls_bos(OXM):#
	fieldlength   = 1
	fieldvalue    = 0x24
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x8847), OXM_eth_type(0x8848))

class OXM_pbb_isid(OXM):#
	fieldlength   = 24
	fieldvalue    = 0x25
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x8847))

class OXM_tunnel_id(OXM):#
	fieldlength   = 64
	fieldvalue    = 0x26
	hasmask       = 0

class OXM_ipv6_hexthdr(OXM):#
	fieldlength   = 9
	fieldvalue    = 0x27
	hasmask       = 0
	_dependencies = (OXM_eth_type(0x86dd))

