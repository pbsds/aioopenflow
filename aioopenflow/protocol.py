from aioopenflow.message import is_msg, MessageType_to_Message, MessageError
from aioopenflow.constants import getMessageType

import asyncio, logging
logger = logging.getLogger('aioopenflow')

class OpenFlowProtocol(asyncio.Protocol):
	def __init__(self, loop, handler, *args, **kwargs):
		asyncio.Protocol.__init__(self, *args, **kwargs)
		
		self.loop = loop
		self.handler = handler(self, loop)
		self.transport = None
		
		self.buffer = b""#ew
	def connection_made(self, transport):
		self.peername = transport.get_extra_info('peername')
		logger.info(f"connection_made from {self.peername}")
		
		self.transport = transport
		
		self.handler.connection_made()
	def connection_lost(self, exc):
		logger.info(f"connection_lost from {self.peername}")
		self.handler.connection_lost(exc)
	def data_received(self, data):
		self.buffer += data#ew
		
		while len(self.buffer) >= 4:
			msg_len = int.from_bytes(self.buffer[2:4], byteorder='big')
			if msg_len <= len(self.buffer):
				msg = self.decode_message(self.buffer[:msg_len])
				self.buffer = self.buffer[msg_len:]#ew
				
				try:
					self.handler.handle_message(msg)
				except NotImplementedError as e:
					logger.warning("NotImplementedError: ")
					logger.warning(e, exc_info = True)
					
			else:
				break
		
		#self.transport.close()
	def decode_message(self, data):
		"""Decodes the bytestring, returning a Message object"""
		assert type(data) is bytes
		
		msg_version = data[0]
		msg_type = getMessageType(msg_version, data[1])
		
		msg = MessageType_to_Message[msg_type]()
		msg.version = msg_version
		msg.unpack(data)
		
		return msg
	def send_message(self, msg):
		assert is_msg(msg)
		if self.handler.version is not None:
			msg.version = self.handler.version
		self.transport.write(msg.pack())
		logger.debug(f"protocol.send_message( {msg} )")
		#print(msg.pack())
	def send_error_message(self, errorcode, xid, errordata=b"", version = None):
		msg = MessageError(errorcode, errordata, xid=xid)
		if version:
			msg.version = version
			
		logger.error(f"protocol.send_error_message( {errorcode} )")
		self.send_message(msg)
		self.transport.close()
