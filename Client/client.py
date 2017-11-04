import socket,sys,base64,json

#creating a socket object
s=socket.socket();
port =21611			#Microsoft 21611		#Google-21609				# Amazon - 21610
host ='40.117.38.107' 				#Microsoft '52.168.141.30' 					#Google -'35.202.28.34'						#Amazon - '18.221.59.87' 	
print (host)
s.connect((host,port))
print "socket created"
filename=sys.argv[1]
size = bytes(len(filename));
b64Data=""
try:
	with open(filename, "rb") as imageFile:
		b64Data = base64.b64encode(imageFile.read())
	JsonOfFile=json.dumps({"Type":"ClientUpload","Name":filename,"size":size})
	s.send(JsonOfFile)
	JsonData=json.dumps({"data":b64Data})
	s.send(JsonData)
	s.close() 
except Exception:
	print("Improper File Name")    
	s.close();
