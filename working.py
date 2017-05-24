import logging
from aioopenflow.server import run
from aioopenflow.handler import BaseHandler
from aioopenflow.constants import openflow10, PORT_ID_Flood
from aioopenflow.message import MessagePacketOut, MessageFlowMod
from aioopenflow.action import ActionOutput
from aioopenflow.match import from_ethernet_packet, from_ip_packet
from aioopenflow.packet import EthernetPacket

#The commands i used when testing this with mininet:
#	ssh mininet@mininet-vm.local
#	sudo mn --topo single,3 --mac --switch ovsk --controller=remote,ip=192.168.56.1

class Openflow10Hub(BaseHandler):
	supported_versions = frozenset((openflow10,))
	def handle_PacketIn(self, msg):
		if msg.reason == "NoMatch":
			print(f"switch {self.switch_datapath_id} from port {msg.in_port}:")
		
			out = MessagePacketOut()
			out.from_PacketIn(msg)
			out.actions.append(ActionOutput(PORT_ID_Flood))
			
			self.protocol.send_message(out)

class Openflow10Switch(BaseHandler):
	supported_versions = frozenset((openflow10,))
	def connection_established(self):
		self.macs = {}
	def handle_PacketIn(self, msg):
		if msg.reason == "NoMatch":
			print(f"switch {self.switch_datapath_id} from port {msg.in_port}:")
			
			packet = EthernetPacket(msg.packet_data)
			self.macs[packet.dl_src] = msg.in_port
			
			if packet.dl_dst not in self.macs:
				out = MessagePacketOut()
				out.from_PacketIn(msg)
				out.actions.append(ActionOutput(PORT_ID_Flood))
				self.protocol.send_message(out)
			else:
				if msg.in_port == self.macs[packet.dl_dst]:
					return
				out = MessageFlowMod()
				
				out.match = from_ethernet_packet(packet, in_port = msg.in_port)
				
				out.command = "Add"
				#out.idle_timeout = 10
				out.buffer_id = msg.buffer_id
				out.hard_timeout = 10
				#out.flags = ("SendFlowRem",)
				
				out.out_port = self.macs[packet.dl_dst]
				out.actions.append(ActionOutput(self.macs[packet.dl_dst]))
				self.protocol.send_message(out)
				
				if msg.buffer_id == -1 and 0:
					out = MessagePacketOut()
					out.from_PacketIn(msg)
					out.actions.append(ActionOutput(self.macs[packet.dl_dst]))
					self.protocol.send_message(out)
		else:
			print(msg.reason)


logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)
#run("0.0.0.0", 6653, handler = Openflow10Hub)
run("0.0.0.0", 6653, handler = Openflow10Switch)
