import socket,os,sys,json,base64,time

class Servers:
	alive=True;
	time=time.time();
	def __init__ (self ,host,port,provider):
		self.host=host
		self.port=port
		self.provider=provider

