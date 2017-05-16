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
		return f"Port({self.port_id}, {self.hw_addr}, {self.name}, {self.config}, {self.state}, {self.feature_curr}, {self.feature_advertised}, {self.feature_supported}, {self.feature_peer})"
	__repr__ = __str__

