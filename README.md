# aioopenflow
A openflow controller implemented using asyncio in Python 3.6. A small project for when I mess 
around with SDN. aioopenflow is designed to be provide an almost identical interface for all 
the different openflow versions between v1.0 to v1.4.

I'm not currently working on this anymore.

### status
This is far from being a usable implementation of openflow, but it lays down the groundwork for 
a simple interface which should be working across multiple openflow version. A lot of the 
different message types, action types, capabilities, ports and matching types have been defined, 
and mainly lacks implementation.

Have a look in *working.py* to see example use

### Probably working:
* Establishing main connections for all openflow versions.
* Decoding switch status and features (of1.0 only)
* Send messages
* Parse error messages (of1.0 only)
* Handle/use EchoReq, PacketIn, PacketOut and FlowMod (of1.0 only)
* Laid groundwork for extensible matching
	* of1.0 reads from the extensible matching headers. (with of1.1 planned as well)
* logging of events
* Simple packet header parsing (ethernet, ip, tcp/udp)

### Todo:
* Make a proper package out of this (setup.py)
* Documentation
* Implement all the message types across the different openflow versions
* Implement all the action types across the different openflow versions
* implement matches for openflow v1.1 and OXM for v1.2 and up
* Add helper functions which can build different matches and such for you.
* switch over from using int.to_bytes() to using struct.pack()

### Released under
GNU GPL v3.0
