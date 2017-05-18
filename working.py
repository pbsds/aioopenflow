import logging
from aioopenflow.server import run
from aioopenflow.handler import BaseHandler
from aioopenflow.constants import openflow10, PORT_ID_Flood
from aioopenflow.message import MessagePacketOut
from aioopenflow.action import ActionOutput

#ssh mininet@192.168.56.101

#sudo mn --topo single,3 --mac --switch ovsk --controller=remote,ip=192.168.56.102

#import aioopenflow.constants
#print(dir(aioopenflow.constants))
#print(aioopenflow.constants.ER_HelloFailed.Incompatible)

class Openflow10Hub(BaseHandler):
	supported_versions = frozenset((openflow10,))
	def connection_established(self):
		for i in self.FeatureRes.ports:
			print(i)
			print()
	def handle_PacketIn(self, msg):
		if msg.reason == "NoMatch":
			out = MessagePacketOut()
			out.from_PacketIn(msg)
			out.actions.append(ActionOutput(PORT_ID_Flood))
			
			self.protocol.send_message(out)

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)
run("0.0.0.0", 6653, handler = Openflow10Hub)#, asyncio_debug=True)
