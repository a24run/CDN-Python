import socket,os,sys,json,base64

class ServerPrices:
	price=100;
	def __init__ (self ,host,port):
		self.host=host
		self.port=port
	def getPrice(self):
		return (self.host,self.port,self.price)
	def setPrice(self,price):
		self.price=price;
		return self.price
