
class PacketBase:
	def _field_int(start, end):
		def fget(self):
			return int(int.from_bytes(self.data[start:end], byteorder='big'))
		def fset(self, value):
			self.data = self.data[:start] + value.to_bytes(end - start, byteorder="big") + self.data[end:]
		return property(fget, fset)
	def _field_iterable(start, end, typefunc=tuple):
		def fget(self):
			return typefunc(self.data[start:end])
		def fset(self, value):
			self.data = self.data[:start] + bytes(value) + self.data[end:]
		return property(fget, fset)
	def __init__(self, packet):
		if issubclass(packet.__class__, PacketBase):
			self.data = packet.data
		else:
			self.data = packet

class EthernetPacket(PacketBase):
	dl_dst  = PacketBase._field_iterable( 0,  6)#Ethernet destination address
	dl_src  = PacketBase._field_iterable( 6, 12)#Ethernet source address
	dl_type = PacketBase._field_int     (12, 14)#Ethernet frame type

class IpPacket(EthernetPacket):
	def __init__(self, packet):
		EthernetPacket.__init__(self, packet)
		assert self.dl_type == 0x0800
		assert (self.nw_head >> 4) == 4#ipv4
	
	nw_head  = PacketBase._field_int     (14, 15)#version and internet header length (4 bits each)
	nw_tos   = PacketBase._field_int     (15, 16)#IP ToS (actually DSCP field, 6 bits) and ECN(2 bits)
	nw_proto = PacketBase._field_int     (23, 24)#IP protocol
	nw_src   = PacketBase._field_iterable(26, 30)#IP source address
	nw_dst   = PacketBase._field_iterable(30, 34)#IP destination address

#dl_vlan  = _field_int(, )#Input VLAN id
#dl_pcp   = _field_int(, )#Input VLAN priority

class TcpIpPacket(IpPacket):#this removes the optional headers
	def __init__(self, packet):
		IpPacket.__init__(self, packet)
		assert self.nw_proto in (0x06, 0x11)
		
		ihl = self.nw_head & 0x0F
		if ihl > 5:#i don't care about ip options
			#todo: care
			self.data = self.data[:34] + self.data[34+(ihl-5)*4:]
	
	tp_src = PacketBase._field_int(34, 36)#TCP/UDP source port
	tp_dst = PacketBase._field_int(36, 38)#TCP/UDP destination port

UdpIpPacket = TcpIpPacket#alias