import socket,os,sys,json,base64

class PriceInfoClass:

	def __init__ (self ,provider,network_hourly_cost,server_hourly_cost):
		self.provider=provider
		self.network_hourly_cost=network_hourly_cost
		self.server_hourly_cost=server_hourly_cost
