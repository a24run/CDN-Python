import socket,os,sys,json,base64,time

class ServerPrices:
	#price=100;
	alive=True;
	time=time.time();
	def __init__ (self ,host,port,provider):
		self.host=host
		self.port=port
		self.provider=provider;
	def getPrice(self):
		return (self.host,self.port,self.price)
	def setPrice(self,price):
		self.price=price;
		return self.price
