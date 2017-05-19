import logging
from aioopenflow.server import run
from aioopenflow.handler import BaseHandler
from aioopenflow.constants import openflow10, PORT_ID_Flood
from aioopenflow.message import MessagePacketOut
from aioopenflow.action import ActionOutput
from aioopenflow.types import TcpIpPacket

#ssh mininet@192.168.56.101
#sudo mn --topo single,3 --mac --switch ovsk --controller=remote,ip=192.168.56.102

class Openflow10Hub(BaseHandler):
	supported_versions = frozenset((openflow10,))
	def connection_established(self):
		#for i in self.switch_ports.values():
		#	print(i)
		#	print()
		pass
	def handle_PacketIn(self, msg):
		if msg.reason == "NoMatch":
			print(f"switch {self.switch_datapath_id} from port {msg.in_port}")
			
			out = MessagePacketOut()
			out.from_PacketIn(msg)
			out.actions.append(ActionOutput(PORT_ID_Flood))
			
			self.protocol.send_message(out)
			
			packet = TcpIpPacket(out.packet_data)
			print("dl_dst   :", packet.dl_dst  )
			print("dl_src   :", packet.dl_src  )
			print("dl_type  :", packet.dl_type )
			print("nw_tos   :", packet.nw_tos  )
			print("nw_proto :", packet.nw_proto)
			print("nw_src   :", packet.nw_src  )
			print("nw_dst   :", packet.nw_dst  )
			print("tp_src   :", packet.tp_src  )
			print("tp_dst   :", packet.tp_dst  )
			print()
	

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)
run("0.0.0.0", 6653, handler = Openflow10Hub)#, asyncio_debug=True)
