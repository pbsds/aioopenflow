import aioopenflow.constants

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

class Port:#currently only supports openflow v1.0
	port_id = 0
	hw_addr = b"\0"*6
	name = ""
	#config
	#state
	#curr
	#advertised
	#supported
	#peer
	def __init__(self, version):
		self.version = version
	def pack(self):#untested
		assert type(self.name) is bytes
		assert type(self.hw_addr) is bytes
		assert len(self.name) <= 15
		assert len(self.hw_addr) == 6
		
		if self.version == aioopenflow.constants.openflow10:#openflow 1.0
			out = (
				(self.port_id & 0xffff).to_bytes(2, byteorder='big'),
				self.hw_addr,
				self.name.encode("ascii"), b"\0" * (16 - len(self.name)),
				
			)
		elif self.version <= aioopenflow.constants.openflow12:#openflow 1.1 and 1.2
			raise
		
		return b"".join(out)
	def unpack(self, data):
		
		self.port_id    = int.from_bytes(data[ 0: 2], byteorder='big')
		self.hw_addr    = data[ 2: 8]
		self.name       = data[ 8:24].split(b"\0", 1)[0].decode("ascii")
		
		config     = int.from_bytes(data[24:28], byteorder='big')
		state      = int.from_bytes(data[28:32], byteorder='big')
		curr       = int.from_bytes(data[32:36], byteorder='big')
		advertised = int.from_bytes(data[36:40], byteorder='big')
		supported  = int.from_bytes(data[40:44], byteorder='big')
		peer       = int.from_bytes(data[44:48], byteorder='big')
		
		if self.version == aioopenflow.constants.openflow10:
			if self.port_id | 0xffff0000 in aioopenflow.constants.PORTS:
				self.port_id |= 0xffff0000
		elif self.version <= aioopenflow.constants.openflow12:
			pass
			
		return self