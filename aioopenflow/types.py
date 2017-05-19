import aioopenflow.constants

#constant types:
class MessageType(tuple):
	def __repr__(self):
		return f"MessageType/{self.name}"
	__str__ = __repr__
	def for_version(self, version, silence=False):
		if not (1<=version<=5):
			raise Exception("Invalid openflow version number %i" % version)
		if not silence:
			if self[version-1] == -1:
				raise Exception("%s is not a valid MessageType in openflow v1.%i" % (self.name, version-1))
		return self[version-1]
	
	@property
	def name(self):
		return self[5]

class ActionType(tuple):
	def __repr__(self):
		return f"ActionType/{self.name}"
	__str__ = __repr__
	def for_version(self, version, silence=False):
		if not (1<=version<=5):
			raise Exception("Invalid openflow version number %i" % version)
		if not silence:
			if self[version-1] == -1:
				raise Exception("%s is not a valid ActionType in openflow v1.%i" % (self.name, version-1))
		return self[version-1]
	
	@property
	def name(self):
		return self[5]

class ErrorType(object):
	def __init__(self, of10type, of11type, of12type, of13type, of14type, name):
		self._types = (of10type, of11type, of12type, of13type, of14type)
		self._name = name
	def __setattr__(self, key, value):
		if key[0] != "_":
			assert type(value) is ErrorCode, f"ErrorType tried setting attribute \"{key}\" of type {type(value)}"
			value.types = self._types
			value.typename = self._name
			value.name = key
		object.__setattr__(self, key, value)
	
class ErrorCode:
	def __init__(self, of10code, of11code, of12code, of13code, of14code):
		self.codes = (of10code, of11code, of12code, of13code, of14code)
		self.types = None#set by ErrorType.__setattribute__
		self.typename = None#set by ErrorType.__setattribute__
		self.name = None#set by ErrorType.__setattribute__
	def __repr__(self):
		return f"Error({self.typename}, {self.name})"
	__str__ = __repr__
	def for_version(self, version):
		if not (1<=version<=5):
			raise Exception("Invalid openflow version number %i" % version)
		if self.codes[version-1] == None:
			raise Exception("%s not a valid ErrorCode in openflow v1.%i" % (self.name, version-1))
		return self.types[version-1], self.codes[version-1]

class NamedInt(int):
	def __new__(cls, value, name, *args, **kwargs):
		self = super(NamedInt, cls).__new__(cls, value, *args, **kwargs)
		self.name = name
		return self
	def __str__(self):
		return self.name
	def __repr__(self):
		#return self.name#lolwatever
		return f"{self.name}:{int(self)}"
		#return f"NamedInt({int(self)}, {self.name})"

#class IpAddress(int):
#	def __new__(cls, value, *args, **kwargs):
#		if type(value) is int:
#			a = (value>>24) & 0xff
#			b = (value>>16) & 0xff
#			c = (value>> 8) & 0xff
#			d = (value    ) & 0xff
#		else:
#			a, b, c, d = value
#			value = (a<<24) | (b<<16) | (c<<8) | d
#		
#		self = super(IpAddress, cls).__new__(cls, value, *args, **kwargs)
#		self._ip = tuple(a, b, c, d)
#		
#		return self
#	def __str__(self):
#		return f"ip{self._ip}"
#	__repr__ = __str__#deprecate?

class TcpIpPacket:
	def _field(start, end, type=int, decode=True):
		def fget(self):
			if decode:
				return type(int.from_bytes(self.data[start:end], byteorder='big'))
			else:
				return type(self.data[start:end])
		def fset(self, value):
			if decode:
				store = value.to_bytes(end - start, byteorder="big")
			else:
				store = bytes(value)
			self.data = self.data[:start] + store + self.data[end:]
		return property(fget, fset)
	def __init__(self, data):
		self.data = data
		assert data[14] == ord("E")#nasty
	
	#assumtions:
	dl_dst   = _field( 0,  6, type=tuple, decode=False) #Ethernet destination address
	dl_src   = _field( 6, 12, type=tuple, decode=False) #Ethernet source address
	#dl_vlan  = _field(, )                               #Input VLAN id
	#dl_pcp   = _field(, )                               #Input VLAN priority
	dl_type  = _field(12, 14)                           #Ethernet frame type
	nw_tos   = _field(15, 16)                           #IP ToS (actually DSCP field, 6 bits) (lacks a >> 2)
	nw_proto = _field(23, 24)                           #IP protocol
	nw_src   = _field(26, 30, type=tuple, decode=False) #IP source address
	nw_dst   = _field(30, 34, type=tuple, decode=False) #IP destination address
	tp_src   = _field(34, 36)                           #TCP/UDP source port
	tp_dst   = _field(36, 38)                           #TCP/UDP destination port
	
	


b'\xda6\x96\x07\xaaY.\x15\xe4\xcb\x18\xb2\x08\x00'
b'E\x00\x00T.\xe9@\x00@\x01\xf7'
b'\xbc\n\x00\x00\x01\n\x00\x00\x03\x08\x00?}\x18)\x00\x01\xf6\x17\x1fY\x9f\xe4\x00'
b'\x00\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b'
b'\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'

#stuff
class Port:#currently only supports openflow v1.0, but lays the groundwork for v1.1 - v1.3
	port_id = 0
	hw_addr = b"\0"*6
	name = ""
	config = frozenset()
	state  = frozenset()
	feature_curr       = frozenset()
	feature_advertised = frozenset()
	feature_supported  = frozenset()
	feature_peer       = frozenset()
	def __init__(self, version):
		self.version = version
	def pack(self):#wip
		raise Warning("Port.pack() is wip")
		
		assert type(self.name) is bytes
		assert type(self.hw_addr) is bytes
		assert len(self.name) <= 15
		assert len(self.hw_addr) == 6
		
		if self.version == aioopenflow.constants.openflow10:#openflow 1.0
			features = ()
			out = (
				(self.port_id & 0xffff).to_bytes(2, byteorder='big'),
				self.hw_addr,
				self.name.encode("ascii"), b"\0" * (16 - len(self.name)),
				
			)
		elif self.version <= aioopenflow.constants.openflow13:#openflow 1.1 - 1.3
			raise NotImplementedError()
		
		return b"".join(out)
	def unpack(self, data):
		self.port_id    = int.from_bytes(data[ 0: 2], byteorder='big')
		self.hw_addr    = data[ 2: 8]
		self.name       = data[ 8:24].split(b"\0", 1)[0].decode("ascii")
		
		config     = int.from_bytes(data[24:28], byteorder='big')
		state      = int.from_bytes(data[28:32], byteorder='big')
		self.config = frozenset(name for bit, name in aioopenflow.constants.PORT_CONFIG.items()               if bit & config)
		self.state  = frozenset(name for bit, name in aioopenflow.constants.PORT_STATES[self.version].items() if bit & state)
		
		curr       = int.from_bytes(data[32:36], byteorder='big')
		advertised = int.from_bytes(data[36:40], byteorder='big')
		supported  = int.from_bytes(data[40:44], byteorder='big')
		peer       = int.from_bytes(data[44:48], byteorder='big')
		
		if self.version == aioopenflow.constants.openflow10:
			if self.port_id | 0xffff0000 in aioopenflow.constants.PORT_IDS:
				self.port_id |= 0xffff0000
			
			curr       = curr       & 0x7f | ((curr      <<4) & 0xfffff800)
			advertised = advertised & 0x7f | ((advertised<<4) & 0xfffff800)
			supported  = supported  & 0x7f | ((supported <<4) & 0xfffff800)
			peer       = peer       & 0x7f | ((peer      <<4) & 0xfffff800)
		elif self.version <= aioopenflow.constants.openflow13:
			raise NotImplementedError()

		self.feature_curr       = frozenset(name for bit, name in aioopenflow.constants.PORT_FEATURE.items() if bit & curr      )
		self.feature_advertised = frozenset(name for bit, name in aioopenflow.constants.PORT_FEATURE.items() if bit & advertised)
		self.feature_supported  = frozenset(name for bit, name in aioopenflow.constants.PORT_FEATURE.items() if bit & supported )
		self.feature_peer       = frozenset(name for bit, name in aioopenflow.constants.PORT_FEATURE.items() if bit & peer      )
		
		#makes the __str__ look nice:
		if self.port_id in aioopenflow.constants.PORT_IDS:
			self.port_id = aioopenflow.constants.PORT_IDS[aioopenflow.constants.PORT_IDS.index(self.port_id)]
		
		return self
	@staticmethod
	def length(version):
		return {
			aioopenflow.constants.openflow10 : 48,
			aioopenflow.constants.openflow11 : 64,
			aioopenflow.constants.openflow12 : 64,
			aioopenflow.constants.openflow13 : 64,
			aioopenflow.constants.openflow14 : 0,
		}[version]
	def __str__(self):
		return f"Port{(self.port_id,self.hw_addr,self.name,self.config,self.state,self.feature_curr,self.feature_advertised,self.feature_supported,self.feature_peer)}"
	__repr__ = __str__
