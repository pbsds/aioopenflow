import logging
from aioopenflow.server import run
from aioopenflow.handler import Openflow10HubHandler

#ssh mininet@192.168.56.101

#sudo mn --topo single,3 --mac --switch ovsk --controller=remote,ip=192.168.56.102

#import aioopenflow.constants
#print(dir(aioopenflow.constants))
#print(aioopenflow.constants.ER_HelloFailed.Incompatible)

logging.basicConfig(level=logging.INFO)
run("0.0.0.0", 6653, handler = Openflow10HubHandler)#, asyncio_debug=True)
