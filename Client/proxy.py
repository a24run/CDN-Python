import sys, os, socket,json,base64,requests,time
from thread import *;
port=8888
max_connection=10;
buffer_size=8192;
class ServerMeasurments:
	def __init__ (self ,host,port,price):
		self.host=host
		self.port=port
		self.price=price
		self.network=0
serverObjects=[]
def initalizeServerObjects():
	del serverObjects[:]
	r = requests.get('http://18.216.195.219:21610/priceInfo')		#http://18.221.59.87:21610/priceInfo
	Servers=r.json()
	for x in range(0,len(Servers["serversWithPrice"])):
		temp=ServerMeasurments(Servers["serversWithPrice"][x]['Host'],Servers["serversWithPrice"][x]['Port'],Servers["serversWithPrice"][x]['Price'])
		serverObjects.append(temp)	
def CalculateRTT():
	for x in range (0,len(serverObjects)):
		socketRTT=socket.socket()
		host=serverObjects[x].host
		port=int(serverObjects[x].port)
		start = int (round (time.time() *1000));  #start time
		socketRTT.connect((host,port))
		JsonOfFile=json.dumps({"Type":"RoundTrip","RandomData":";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"});
		socketRTT.send(JsonOfFile)
		somedata=socketRTT.recv(1024)
		elapsed = int (round (time.time() * 1000)) - start # end time 
		serverObjects[x].network=elapsed;
		socketRTT.close();
	for x in range(0,len(serverObjects)):
		print("Name , network and price ",serverObjects[x].host,serverObjects[x].network,serverObjects[x].price)			
def start():
	try:
		initalizeServerObjects();
		s=socket.socket()
		host=socket.gethostname();
		s.bind((host,port))
		s.listen(max_connection)
		print ("Proxy server initialised")
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit(2);
	while(1):
		try:
			conn,addr=s.accept();
			data=conn.recv(buffer_size)
			start_new_thread(proxy_server,(conn,data,addr))
		except KeyboardInterrupt:
			s.close();
			print "\n User requested an Interruption"
			print "\n exciting Application"
			sys.exit()
	s.close()
# def conn_string(conn,data,addr):
# 	#print("Connection Recived data is ", data);
# 	ConnectionRequested=data.split(' ')
# 	urlToDownload=ConnectionRequested[1]
# 	httptext= (urlToDownload[0:7]);
# 	if(str(httptext) == "http://"):
# 		hostAndFile=urlToDownload[7:]
# 		[serverRequested,fileName]=hostAndFile.split('/')

# 	else:
# 		print('not a proper URL');
# 	start_new_thread(proxy_server,(conn,fileName,addr))	
	#proxy_server(conn,fileName,addr);
def proxy_server(conn,data,addr):
	CalculateRTT();
	ConnectionRequested=data.split(' ')
	urlToDownload=ConnectionRequested[1]
	httptext= (urlToDownload[0:7]);
	if(str(httptext) == "http://"):
		hostAndFile=urlToDownload[7:]
		[serverRequested,fileName]=hostAndFile.split('/')

	else:
		print('not a proper URL');
	leastPrice=99999;
	leastHost=""
	portLeastHost=0
	if(sys.argv[1] =="price"):
		for x in range (0, len(serverObjects)):
			if(serverObjects[x].price<leastPrice):
				leastPrice=serverObjects[x].price
				leastHost=serverObjects[x].host
				portLeastHost=serverObjects[x].port
	elif(sys.argv[1] =="network"):
		for x in range (0, len(serverObjects)):
			if(serverObjects[x].network<leastPrice):
				leastPrice=serverObjects[x].network
				leastHost=serverObjects[x].host
				portLeastHost=serverObjects[x].port
	elif(sys.argv[1] =="networkPrice"):
		for x in range (0, len(serverObjects)):
			if(serverObjects[x].network<leastPrice):
				leastPrice=serverObjects[x].network +serverObjects[x].price
				leastHost=serverObjects[x].host
				portLeastHost=serverObjects[x].port
	else:
		conn.send('HTTP/1.1 '+'404'+'NAN '+'\n\n')
		conn.send("Not a proper URL")
		conn.close();
	print ("The Best case is",leastHost,"Port is ",portLeastHost,"price is ", leastPrice)
	url='http://'+leastHost+'/'+fileName
	requestToHost=requests.get(url)
	#print('http/1.1 '+str(requestToHost.status_code)+' OK'+'\n'+str(requestToHost.headers['Content-Length'])+'\n'+ str(requestToHost.headers['content-type'])+'\n\n')
	#c.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n");
	if(requestToHost.status_code!=404):
		print('http/1.1 '+str(requestToHost.status_code)+' OK'+'\n')
		conn.send('HTTP/1.1 '+str(requestToHost.status_code)+' OK'+'\n')
		conn.send("Accept-Ranges"+":"+ "bytes" +'\n')
		conn.send("Content-Length:"+str(requestToHost.headers['Content-Length'])+'\n\n')
		#conn.send("Content-Type:"+str(requestToHost.headers['Content-type'])+'\n\n');
		for chunk in requestToHost.iter_content(1024):
			conn.send(chunk)
		conn.close();
	else:
		conn.send('HTTP/1.1 '+str(requestToHost.status_code)+' Not Found'+'\n\n')
		conn.send('FILE NOT FOUND ')
		conn.close();
start();