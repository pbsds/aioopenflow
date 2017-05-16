import asyncio
from aioopenflow.constants import *
from aioopenflow.protocol import OpenFlowProtocol
from aioopenflow.handler import BaseHandler


async def wake_coro():
	"Wakes the event loop every second"
	while 1:
		await asyncio.sleep(1)

def run(host="127.0.0.1", port=6653, handler = BaseHandler, asyncio_debug=False):
	"""Starts """
	
	loop = asyncio.get_event_loop()
	wake = asyncio.ensure_future(wake_coro())
	loop.set_debug(asyncio_debug)
	
	coro = loop.create_server(lambda: OpenFlowProtocol(loop, handler), host, port)
	server = loop.run_until_complete(coro)
	
	#blocking:
	print('Serving on {}\n\n'.format(server.sockets[0].getsockname()))
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	
	#close
	wake.cancel()
	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()
